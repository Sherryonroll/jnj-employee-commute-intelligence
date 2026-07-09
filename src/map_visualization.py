import folium
import pandas as pd
from folium.plugins import MarkerCluster

from config import (
    ADOPTION_OUTPUT_FILE,
    TRANSPORT_STATIONS_FILE,
    MAPS_DIR,
    WORKPLACE_LAT,
    WORKPLACE_LON,
    WORKPLACE_NAME,
    WORKPLACE_ADDRESS,
)


MAP_FILE = MAPS_DIR / "commute_map.html"


ADOPTION_COLORS = {
    "Very High": "green",
    "High": "blue",
    "Medium": "orange",
    "Low": "red",
}


def create_employee_popup(row):
    return f"""
    <b>Employee:</b> {row["employee_id"]}<br>
    <b>Home area:</b> {row["home_area"]}<br>
    <b>Base commute:</b> {row["base_commute_time_min"]} min<br>
    <b>Delay-adjusted commute:</b> {row["risk_adjusted_commute_time_min"]} min<br>
    <b>Adoption potential:</b> {row["adoption_potential"]}<br>
    <b>Adoption score:</b> {row["adoption_score"]}<br>
    <b>Station access:</b> {row["nearest_public_transport_access_m"]} m<br>
    <b>Transfers:</b> {row["number_of_transfers"]}<br>
    <b>Delay impact:</b> {row["delay_impact"]}<br>
    <b>First-mile mode:</b> {row["first_mile_mode"]}
    """


def create_station_popup(row):
    return f"""
    <b>Station:</b> {row["station_name"]}<br>
    <b>Area:</b> {row["area"]}<br>
    <b>Mode:</b> {row["mode"]}<br>
    <b>Lines:</b> {row["lines"]}<br>
    <b>Connectivity score:</b> {row["connectivity_score"]}
    """


def add_workplace_marker(commute_map):
    popup = f"""
    <b>{WORKPLACE_NAME}</b><br>
    {WORKPLACE_ADDRESS}
    """

    folium.Marker(
        location=[WORKPLACE_LAT, WORKPLACE_LON],
        popup=folium.Popup(popup, max_width=300),
        tooltip="Johnson & Johnson Medical GmbH",
        icon=folium.Icon(color="darkred", icon="briefcase", prefix="fa"),
    ).add_to(commute_map)


def add_station_markers(commute_map, stations_df):
    station_layer = folium.FeatureGroup(name="Major public transport stations")

    for _, row in stations_df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(create_station_popup(row), max_width=300),
            tooltip=row["station_name"],
            icon=folium.Icon(color="cadetblue", icon="train", prefix="fa"),
        ).add_to(station_layer)

    station_layer.add_to(commute_map)


def add_employee_markers(commute_map, employees_df):
    employee_layer = folium.FeatureGroup(name="Synthetic employees")
    cluster = MarkerCluster(name="Employee clusters").add_to(employee_layer)

    for _, row in employees_df.iterrows():
        color = ADOPTION_COLORS.get(row["adoption_potential"], "gray")

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(create_employee_popup(row), max_width=350),
            tooltip=f'{row["employee_id"]} | {row["adoption_potential"]}',
            icon=folium.Icon(color=color, icon="user", prefix="fa"),
        ).add_to(cluster)

    employee_layer.add_to(commute_map)


def create_commute_map():
    employees_df = pd.read_csv(ADOPTION_OUTPUT_FILE)
    stations_df = pd.read_csv(TRANSPORT_STATIONS_FILE)

    commute_map = folium.Map(
        location=[53.62, 10.02],
        zoom_start=10,
        tiles="CartoDB positron",
    )

    add_workplace_marker(commute_map)
    add_station_markers(commute_map, stations_df)
    add_employee_markers(commute_map, employees_df)

    folium.LayerControl().add_to(commute_map)

    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    commute_map.save(MAP_FILE)

    return MAP_FILE


def main():
    map_file = create_commute_map()
    print(f"Interactive commute map created: {map_file}")


if __name__ == "__main__":
    main()