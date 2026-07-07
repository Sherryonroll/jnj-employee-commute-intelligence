import numpy as np
import pandas as pd

from config import (
    SYNTHETIC_EMPLOYEES_FILE,
    TRANSPORT_STATIONS_FILE,
    COMMUTE_FEATURES_FILE,
    WORKPLACE_LAT,
    WORKPLACE_LON,
    DELAY_BUFFER_MIN,
    WALKING_SPEED_KMH,
    TRANSFER_PENALTY_MIN,
    RANDOM_SEED,
    DIRECT_WALK_TO_MAJOR_STATION_KM,
    FEEDER_BUS_SPEED_KMH,
    LOCAL_ROUTE_FACTOR,
    AREA_ACCESS_PROFILES,
)

from utils import (
    haversine_distance_km,
    walking_time_min,
    classify_commute_time,
    classify_station_access,
    classify_delay_impact,
)


DESTINATION_STATION = "Norderstedt Mitte"


def estimate_transfers(station_name):
    simple_routes = {
        "Norderstedt Mitte", "Richtweg", "Garstedt", "Ochsenzoll",
        "Langenhorn Markt", "Ohlsdorf", "Kellinghusenstrasse",
        "Hamburg Hbf", "Jungfernstieg", "Wandsbek Markt",
    }

    one_transfer_routes = {
        "Barmbek", "Dammtor", "Altona", "Pinneberg", "Quickborn",
        "Henstedt-Ulzburg", "Kaltenkirchen", "Ahrensburg",
    }

    if station_name in simple_routes:
        return 0
    if station_name in one_transfer_routes:
        return 1
    return 2


def estimate_transit_speed_kmh(mode):
    if "Regional" in mode:
        return 55
    if "AKN" in mode:
        return 42
    if "S-Bahn" in mode:
        return 38
    if "U-Bahn" in mode:
        return 34
    return 28


def estimate_wait_time_min(connectivity_score):
    return float(np.interp(connectivity_score, [0.65, 1.00], [10, 3]))


def employee_seed(employee_id):
    number = int(str(employee_id).replace("EMP", ""))
    return RANDOM_SEED + number


def estimate_local_access(employee, major_station_distance_km):
    profile = AREA_ACCESS_PROFILES.get(
        employee["area_type"],
        AREA_ACCESS_PROFILES["urban"],
    )

    rng = np.random.default_rng(employee_seed(employee["employee_id"]))

    local_access_m = rng.triangular(
        profile["min_m"],
        profile["typical_m"],
        profile["max_m"],
    )

    major_station_distance_m = major_station_distance_km * 1000

    return min(local_access_m, major_station_distance_m), profile["local_wait_min"]


def find_nearest_major_station(employee_row, stations_df):
    distances = haversine_distance_km(
        employee_row["latitude"],
        employee_row["longitude"],
        stations_df["lat"],
        stations_df["lon"],
    )

    nearest_idx = distances.idxmin()
    nearest_station = stations_df.loc[nearest_idx].copy()
    nearest_station["distance_km"] = distances.loc[nearest_idx]

    return nearest_station


def calculate_commute_features(employees_df, stations_df):
    destination_station = stations_df[
        stations_df["station_name"] == DESTINATION_STATION
    ].iloc[0]

    destination_walk_km = haversine_distance_km(
        destination_station["lat"],
        destination_station["lon"],
        WORKPLACE_LAT,
        WORKPLACE_LON,
    )

    records = []

    for _, employee in employees_df.iterrows():
        major_station = find_nearest_major_station(employee, stations_df)

        home_to_work_km = haversine_distance_km(
            employee["latitude"],
            employee["longitude"],
            WORKPLACE_LAT,
            WORKPLACE_LON,
        )

        major_station_distance_km = major_station["distance_km"]

        public_transport_access_m, local_wait_time_min = estimate_local_access(
            employee,
            major_station_distance_km,
        )

        uses_feeder_bus = major_station_distance_km > DIRECT_WALK_TO_MAJOR_STATION_KM

        if uses_feeder_bus:
            first_mile_mode = "Walk to local stop + feeder bus"
            access_walk_km = public_transport_access_m / 1000
            feeder_bus_distance_km = max(
                major_station_distance_km - access_walk_km,
                0,
            ) * LOCAL_ROUTE_FACTOR
            feeder_bus_time_min = (feeder_bus_distance_km / FEEDER_BUS_SPEED_KMH) * 60
            feeder_transfer_count = 1
        else:
            first_mile_mode = "Walk directly to major station"
            access_walk_km = major_station_distance_km
            local_wait_time_min = 0
            feeder_bus_distance_km = 0
            feeder_bus_time_min = 0
            feeder_transfer_count = 0

        station_to_destination_km = haversine_distance_km(
            major_station["lat"],
            major_station["lon"],
            destination_station["lat"],
            destination_station["lon"],
        )

        route_transfer_count = estimate_transfers(major_station["station_name"])
        number_of_transfers = route_transfer_count + feeder_transfer_count

        transit_speed_kmh = estimate_transit_speed_kmh(major_station["mode"])
        major_station_wait_time_min = estimate_wait_time_min(
            major_station["connectivity_score"]
        )

        origin_walk_time_min = walking_time_min(access_walk_km, WALKING_SPEED_KMH)
        destination_walk_time_min = walking_time_min(
            destination_walk_km,
            WALKING_SPEED_KMH,
        )

        route_factor = 1.15
        main_transit_time_min = (
            (station_to_destination_km * route_factor) / transit_speed_kmh
        ) * 60

        transfer_time_min = number_of_transfers * TRANSFER_PENALTY_MIN

        base_commute_time_min = (
            origin_walk_time_min
            + local_wait_time_min
            + feeder_bus_time_min
            + major_station_wait_time_min
            + main_transit_time_min
            + transfer_time_min
            + destination_walk_time_min
        )

        risk_adjusted_commute_time_min = base_commute_time_min + DELAY_BUFFER_MIN

        base_group = classify_commute_time(base_commute_time_min)
        adjusted_group = classify_commute_time(risk_adjusted_commute_time_min)

        records.append(
            {
                "employee_id": employee["employee_id"],
                "home_area": employee["home_area"],
                "area_type": employee["area_type"],
                "latitude": employee["latitude"],
                "longitude": employee["longitude"],
                "home_to_work_km": round(home_to_work_km, 2),
                "major_station_used_for_route": major_station["station_name"],
                "major_station_area": major_station["area"],
                "major_station_mode": major_station["mode"],
                "major_station_lines": major_station["lines"],
                "station_connectivity_score": round(
                    major_station["connectivity_score"], 2
                ),
                "nearest_major_station_distance_m": round(
                    major_station_distance_km * 1000, 0
                ),
                "nearest_public_transport_access_m": round(
                    public_transport_access_m, 0
                ),
                "home_to_station_m": round(public_transport_access_m, 0),
                "station_access_category": classify_station_access(
                    public_transport_access_m
                ),
                "first_mile_mode": first_mile_mode,
                "uses_feeder_bus": uses_feeder_bus,
                "feeder_bus_distance_km": round(feeder_bus_distance_km, 2),
                "feeder_bus_time_min": round(feeder_bus_time_min, 1),
                "number_of_transfers": number_of_transfers,
                "estimated_wait_time_min": round(
                    local_wait_time_min + major_station_wait_time_min, 1
                ),
                "origin_walk_time_min": round(origin_walk_time_min, 1),
                "main_transit_time_min": round(main_transit_time_min, 1),
                "transfer_time_min": round(transfer_time_min, 1),
                "destination_walk_time_min": round(destination_walk_time_min, 1),
                "base_commute_time_min": round(base_commute_time_min, 1),
                "delay_buffer_min": DELAY_BUFFER_MIN,
                "risk_adjusted_commute_time_min": round(
                    risk_adjusted_commute_time_min, 1
                ),
                "base_commute_group": base_group,
                "risk_adjusted_commute_group": adjusted_group,
                "delay_impact": classify_delay_impact(base_group, adjusted_group),
                "crosses_45_min_after_delay": bool(
                    base_commute_time_min <= 45
                    and risk_adjusted_commute_time_min > 45
                ),
            }
        )

    return pd.DataFrame(records)


def main():
    employees_df = pd.read_csv(SYNTHETIC_EMPLOYEES_FILE)
    stations_df = pd.read_csv(TRANSPORT_STATIONS_FILE)

    COMMUTE_FEATURES_FILE.parent.mkdir(parents=True, exist_ok=True)

    commute_df = calculate_commute_features(employees_df, stations_df)
    commute_df.to_csv(COMMUTE_FEATURES_FILE, index=False)

    print(f"Commute feature dataset created: {COMMUTE_FEATURES_FILE}")
    print(f"Number of employees: {len(commute_df)}")

    print("\nBase commute groups:")
    print(commute_df["base_commute_group"].value_counts(normalize=True).mul(100).round(1))

    print("\nRisk-adjusted commute groups:")
    print(
        commute_df["risk_adjusted_commute_group"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
    )

    print("\nStation access categories:")
    print(
        commute_df["station_access_category"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
    )

    print("\nDelay impact:")
    print(commute_df["delay_impact"].value_counts(normalize=True).mul(100).round(1))


if __name__ == "__main__":
    main()