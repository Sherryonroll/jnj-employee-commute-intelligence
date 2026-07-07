import numpy as np
import pandas as pd

from config import (
    N_EMPLOYEES,
    RANDOM_SEED,
    SYNTHETIC_EMPLOYEES_FILE,
)


AREA_PROFILES = [
    {"home_area": "Norderstedt", "lat": 53.7070, "lon": 9.9950, "weight": 0.16, "radius_km": 4.0, "area_type": "near_workplace"},
    {"home_area": "Hamburg-City", "lat": 53.5511, "lon": 9.9937, "weight": 0.10, "radius_km": 4.0, "area_type": "urban"},
    {"home_area": "Hamburg-Altona", "lat": 53.5500, "lon": 9.9350, "weight": 0.08, "radius_km": 4.0, "area_type": "urban"},
    {"home_area": "Hamburg-Eimsbuettel", "lat": 53.5744, "lon": 9.9565, "weight": 0.08, "radius_km": 3.5, "area_type": "urban"},
    {"home_area": "Hamburg-Wandsbek", "lat": 53.5833, "lon": 10.0833, "weight": 0.10, "radius_km": 5.0, "area_type": "urban"},
    {"home_area": "Hamburg-Barmbek", "lat": 53.5890, "lon": 10.0440, "weight": 0.07, "radius_km": 3.5, "area_type": "urban"},
    {"home_area": "Hamburg-Harburg", "lat": 53.4600, "lon": 9.9830, "weight": 0.05, "radius_km": 5.0, "area_type": "outer_urban"},
    {"home_area": "Pinneberg", "lat": 53.6590, "lon": 9.7990, "weight": 0.07, "radius_km": 4.5, "area_type": "suburban"},
    {"home_area": "Quickborn", "lat": 53.7290, "lon": 9.9020, "weight": 0.07, "radius_km": 4.0, "area_type": "suburban"},
    {"home_area": "Ahrensburg", "lat": 53.6750, "lon": 10.2400, "weight": 0.05, "radius_km": 4.5, "area_type": "suburban"},
    {"home_area": "Henstedt-Ulzburg", "lat": 53.7910, "lon": 9.9840, "weight": 0.05, "radius_km": 5.0, "area_type": "outer_suburban"},
    {"home_area": "Kaltenkirchen", "lat": 53.8370, "lon": 9.9620, "weight": 0.04, "radius_km": 5.0, "area_type": "outer_suburban"},
    {"home_area": "Elmshorn", "lat": 53.7540, "lon": 9.6530, "weight": 0.04, "radius_km": 5.0, "area_type": "outer_suburban"},
    {"home_area": "Bad Oldesloe", "lat": 53.8110, "lon": 10.3740, "weight": 0.02, "radius_km": 4.5, "area_type": "regional"},
    {"home_area": "Lueneburg", "lat": 53.2470, "lon": 10.4140, "weight": 0.02, "radius_km": 5.0, "area_type": "regional"},
]


def generate_random_point(center_lat, center_lon, radius_km, rng):
    """Generate a random point around an area center within a realistic local radius."""
    angle = rng.uniform(0, 2 * np.pi)
    distance = radius_km * np.sqrt(rng.uniform(0, 1))

    delta_lat = (distance * np.cos(angle)) / 111
    delta_lon = (distance * np.sin(angle)) / (111 * np.cos(np.radians(center_lat)))

    return center_lat + delta_lat, center_lon + delta_lon


def generate_synthetic_employees(n_employees=N_EMPLOYEES, random_seed=RANDOM_SEED):
    rng = np.random.default_rng(random_seed)

    weights = np.array([area["weight"] for area in AREA_PROFILES])
    weights = weights / weights.sum()

    selected_area_idx = rng.choice(len(AREA_PROFILES), size=n_employees, p=weights)

    records = []

    for i, area_idx in enumerate(selected_area_idx, start=1):
        area = AREA_PROFILES[area_idx]

        lat, lon = generate_random_point(
            center_lat=area["lat"],
            center_lon=area["lon"],
            radius_km=area["radius_km"],
            rng=rng,
        )

        records.append(
            {
                "employee_id": f"EMP{i:04d}",
                "home_area": area["home_area"],
                "area_type": area["area_type"],
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
            }
        )

    return pd.DataFrame(records)


def main():
    SYNTHETIC_EMPLOYEES_FILE.parent.mkdir(parents=True, exist_ok=True)

    employees_df = generate_synthetic_employees()
    employees_df.to_csv(SYNTHETIC_EMPLOYEES_FILE, index=False)

    print(f"Synthetic employee dataset created: {SYNTHETIC_EMPLOYEES_FILE}")
    print(f"Number of employees: {len(employees_df)}")
    print("\nEmployees by area:")
    print(employees_df["home_area"].value_counts().sort_values(ascending=False))
    print("\nSample rows:")
    print(employees_df.head())


if __name__ == "__main__":
    main()