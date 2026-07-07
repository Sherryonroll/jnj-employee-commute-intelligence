import numpy as np


def haversine_distance_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two latitude/longitude points in kilometers."""
    earth_radius_km = 6371

    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (
        np.sin(delta_lat / 2) ** 2
        + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon / 2) ** 2
    )

    c = 2 * np.arcsin(np.sqrt(a))
    return earth_radius_km * c


def walking_time_min(distance_km, walking_speed_kmh=4.8):
    """Convert walking distance into walking time."""
    return (distance_km / walking_speed_kmh) * 60


def classify_commute_time(minutes):
    if minutes <= 30:
        return "0-30 min"
    if minutes <= 45:
        return "31-45 min"
    if minutes <= 60:
        return "46-60 min"
    return "60+ min"


def classify_station_access(distance_m):
    if distance_m <= 500:
        return "Excellent"
    if distance_m <= 1000:
        return "Good"
    if distance_m <= 1500:
        return "Acceptable"
    return "Poor"


def classify_delay_impact(base_group, adjusted_group):
    group_order = {
        "0-30 min": 0,
        "31-45 min": 1,
        "46-60 min": 2,
        "60+ min": 3,
    }

    movement = group_order[adjusted_group] - group_order[base_group]

    if movement <= 0:
        return "No impact"
    if movement == 1:
        return "Minor impact"
    return "Major impact"