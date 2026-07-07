import pandas as pd

from config import TRANSPORT_STATIONS_FILE


TRANSPORT_STATIONS = [
    {"station_name": "Norderstedt Mitte", "area": "Norderstedt", "lat": 53.7080, "lon": 9.9928, "mode": "U-Bahn / AKN", "lines": "U1, A2", "connectivity_score": 0.95},
    {"station_name": "Richtweg", "area": "Norderstedt", "lat": 53.6950, "lon": 9.9950, "mode": "U-Bahn", "lines": "U1", "connectivity_score": 0.85},
    {"station_name": "Garstedt", "area": "Norderstedt", "lat": 53.6830, "lon": 9.9940, "mode": "U-Bahn", "lines": "U1", "connectivity_score": 0.85},
    {"station_name": "Ochsenzoll", "area": "Hamburg-Langenhorn", "lat": 53.6770, "lon": 10.0010, "mode": "U-Bahn", "lines": "U1", "connectivity_score": 0.80},
    {"station_name": "Langenhorn Markt", "area": "Hamburg-Langenhorn", "lat": 53.6490, "lon": 10.0170, "mode": "U-Bahn", "lines": "U1", "connectivity_score": 0.80},
    {"station_name": "Ohlsdorf", "area": "Hamburg-Ohlsdorf", "lat": 53.6210, "lon": 10.0310, "mode": "U-Bahn / S-Bahn", "lines": "U1, S1", "connectivity_score": 0.95},
    {"station_name": "Barmbek", "area": "Hamburg-Barmbek", "lat": 53.5870, "lon": 10.0440, "mode": "U-Bahn / S-Bahn", "lines": "U3, S1", "connectivity_score": 0.90},
    {"station_name": "Kellinghusenstrasse", "area": "Hamburg-Eppendorf", "lat": 53.5880, "lon": 9.9900, "mode": "U-Bahn", "lines": "U1, U3", "connectivity_score": 0.90},
    {"station_name": "Hamburg Hbf", "area": "Hamburg-City", "lat": 53.5527, "lon": 10.0067, "mode": "U-Bahn / S-Bahn / Regional", "lines": "U1, U2, U3, U4, S-Bahn, RE", "connectivity_score": 1.00},
    {"station_name": "Jungfernstieg", "area": "Hamburg-City", "lat": 53.5520, "lon": 9.9940, "mode": "U-Bahn / S-Bahn", "lines": "U1, U2, U4, S1, S3", "connectivity_score": 0.95},
    {"station_name": "Dammtor", "area": "Hamburg-City", "lat": 53.5608, "lon": 9.9892, "mode": "S-Bahn / Regional", "lines": "S-Bahn, RE", "connectivity_score": 0.90},
    {"station_name": "Altona", "area": "Hamburg-Altona", "lat": 53.5520, "lon": 9.9350, "mode": "S-Bahn / Regional", "lines": "S1, S2, S3, RE", "connectivity_score": 0.95},
    {"station_name": "Wandsbek Markt", "area": "Hamburg-Wandsbek", "lat": 53.5720, "lon": 10.0670, "mode": "U-Bahn / Bus", "lines": "U1, Bus", "connectivity_score": 0.85},
    {"station_name": "Harburg", "area": "Hamburg-Harburg", "lat": 53.4560, "lon": 9.9910, "mode": "S-Bahn / Regional", "lines": "S3, S5, RE", "connectivity_score": 0.90},
    {"station_name": "Pinneberg", "area": "Pinneberg", "lat": 53.6540, "lon": 9.7970, "mode": "S-Bahn / Regional", "lines": "S3, RE", "connectivity_score": 0.80},
    {"station_name": "Quickborn", "area": "Quickborn", "lat": 53.7310, "lon": 9.9040, "mode": "AKN", "lines": "A1", "connectivity_score": 0.70},
    {"station_name": "Henstedt-Ulzburg", "area": "Henstedt-Ulzburg", "lat": 53.7900, "lon": 9.9820, "mode": "AKN", "lines": "A1, A2", "connectivity_score": 0.70},
    {"station_name": "Kaltenkirchen", "area": "Kaltenkirchen", "lat": 53.8370, "lon": 9.9620, "mode": "AKN", "lines": "A1", "connectivity_score": 0.65},
    {"station_name": "Elmshorn", "area": "Elmshorn", "lat": 53.7540, "lon": 9.6530, "mode": "Regional", "lines": "RE", "connectivity_score": 0.70},
    {"station_name": "Ahrensburg", "area": "Ahrensburg", "lat": 53.6750, "lon": 10.2390, "mode": "Regional", "lines": "RE", "connectivity_score": 0.75},
    {"station_name": "Bad Oldesloe", "area": "Bad Oldesloe", "lat": 53.8110, "lon": 10.3740, "mode": "Regional", "lines": "RE", "connectivity_score": 0.65},
    {"station_name": "Lueneburg", "area": "Lueneburg", "lat": 53.2480, "lon": 10.4140, "mode": "Regional", "lines": "RE", "connectivity_score": 0.70},
]


def create_transport_station_dataset():
    stations_df = pd.DataFrame(TRANSPORT_STATIONS)
    return stations_df


def main():
    TRANSPORT_STATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

    stations_df = create_transport_station_dataset()
    stations_df.to_csv(TRANSPORT_STATIONS_FILE, index=False)

    print(f"Transport station dataset created: {TRANSPORT_STATIONS_FILE}")
    print(f"Number of stations: {len(stations_df)}")
    print(stations_df.head())


if __name__ == "__main__":
    main()