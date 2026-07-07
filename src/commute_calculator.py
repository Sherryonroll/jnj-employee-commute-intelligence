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
    direct_or_simple = {
        "Norderstedt Mitte",
        "Richtweg",
        "Garstedt",
        "Ochsenzoll",
        "Langenhorn Markt",
        "Ohlsdorf",
        "Kellinghusenstrasse",
        "Hamburg Hbf",
        "Jungfernstieg",
        "Wandsbek Markt",
    }

    one_transfer = {
        "Barmbek",
        "Dammtor",
        "Altona",
        "Pinneberg",
        "Quickborn",
        "Henstedt-Ulzburg",
        "Kaltenkirchen",
        "Ahrensburg",
    }

    if station_name in direct_or_simple:
        return 0
    if station_name in one_transfer:
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
    # Higher station connectivity means shorter average waiting time.
    return float(np.interp(connectivity_score, [0.65, 1.00], [10, 3]))


def find_nearest_station(employee_row, stations_df):
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
        nearest_station = find_nearest_station(employee, stations_df)

        home_to_work_km = haversine_distance_km(
            employee["latitude"],
            employee["longitude"],
            WORKPLACE_LAT,
            WORKPLACE_LON,
        )

        home_to_station_km = nearest_station["distance_km"]

        station_to_destination_km = haversine_distance_km(
            nearest_station["lat"],
            nearest_station["lon"],
            destination_station["lat"],
            destination_station["lon"],
        )

        transfer_count = estimate_transfers(nearest_station["station_name"])
        transit_speed_kmh = estimate_transit_speed_kmh(nearest_station["mode"])
        wait_time_min = estimate_wait_time_min(nearest_station["connectivity_score"])

        origin_walk_time_min = walking_time_min(home_to_station_km, WALKING_SPEED_KMH)
        destination_walk_time_min = walking_time_min(destination_walk_km, WALKING_SPEED_KMH)

        # Rail routes are usually not perfectly straight, so we apply a realistic route factor.
        route_factor = 1.25
        transit_time_min = (
            (station_to_destination_km * route_factor) / transit_speed_kmh
        ) * 60

        transfer_time_min = transfer_count * TRANSFER_PENALTY_MIN

        base_commute_time_min = (
            origin_walk_time_min
            + wait_time_min
            + transit_time_min
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
                "nearest_station": nearest_station["station_name"],
                "nearest_station_area": nearest_station["area"],
                "nearest_station_mode": nearest_station["mode"],
                "nearest_station_lines": nearest_station["lines"],
                "station_connectivity_score": round(nearest_station["connectivity_score"], 2),
                "home_to_work_km": round(home_to_work_km, 2),
                "home_to_station_m": round(home_to_station_km * 1000, 0),
                "station_access_category": classify_station_access(home_to_station_km * 1000),
                "destination_station_to_work_m": round(destination_walk_km * 1000, 0),
                "number_of_transfers": transfer_count,
                "estimated_wait_time_min": round(wait_time_min, 1),
                "origin_walk_time_min": round(origin_walk_time_min, 1),
                "transit_time_min": round(transit_time_min, 1),
                "transfer_time_min": round(transfer_time_min, 1),
                "destination_walk_time_min": round(destination_walk_time_min, 1),
                "base_commute_time_min": round(base_commute_time_min, 1),
                "delay_buffer_min": DELAY_BUFFER_MIN,
                "risk_adjusted_commute_time_min": round(risk_adjusted_commute_time_min, 1),
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

    print("\nDelay impact:")
    print(commute_df["delay_impact"].value_counts(normalize=True).mul(100).round(1))

    print("\nSample rows:")
    print(commute_df.head())


if __name__ == "__main__":
    main()