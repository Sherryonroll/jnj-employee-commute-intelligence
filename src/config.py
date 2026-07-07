from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

OUTPUTS_DIR = BASE_DIR / "outputs"
CHARTS_DIR = OUTPUTS_DIR / "charts"
MAPS_DIR = OUTPUTS_DIR / "maps"
SUMMARY_DIR = OUTPUTS_DIR / "summary"

# Random seed for reproducibility
RANDOM_SEED = 42

# Synthetic employee settings
N_EMPLOYEES = 1000

# Johnson & Johnson Medical GmbH workplace location
WORKPLACE_NAME = "Johnson & Johnson Medical GmbH"
WORKPLACE_ADDRESS = "Robert-Koch-Strasse 1, 22851 Norderstedt, Germany"

# Approximate coordinates for Robert-Koch-Strasse 1, Norderstedt
WORKPLACE_LAT = 53.7017
WORKPLACE_LON = 9.9846

# Commute thresholds in minutes
COMMUTE_BINS = [0, 30, 45, 60, 999]
COMMUTE_LABELS = ["0-30 min", "31-45 min", "46-60 min", "60+ min"]

# Reliability / delay scenario
DELAY_BUFFER_MIN = 15

# Walking and transfer assumptions
WALKING_SPEED_KMH = 4.8
TRANSFER_PENALTY_MIN = 5

# First-mile public transport assumptions
DIRECT_WALK_TO_MAJOR_STATION_KM = 1.5
FEEDER_BUS_SPEED_KMH = 26
LOCAL_ROUTE_FACTOR = 1.20

# Local HVV access assumptions by area type.
# These represent walking distance to the nearest practical public transport access point.
AREA_ACCESS_PROFILES = {
    "near_workplace": {"min_m": 120, "typical_m": 450, "max_m": 900, "local_wait_min": 5},
    "urban": {"min_m": 150, "typical_m": 550, "max_m": 1100, "local_wait_min": 6},
    "outer_urban": {"min_m": 250, "typical_m": 750, "max_m": 1400, "local_wait_min": 8},
    "suburban": {"min_m": 300, "typical_m": 900, "max_m": 1700, "local_wait_min": 9},
    "outer_suburban": {"min_m": 400, "typical_m": 1100, "max_m": 2200, "local_wait_min": 11},
    "regional": {"min_m": 500, "typical_m": 1400, "max_m": 2800, "local_wait_min": 13},
}

# Public transport access thresholds
STATION_ACCESS_THRESHOLDS_M = {
    "excellent": 500,
    "good": 1000,
    "acceptable": 1500,
}

# Output files
TRANSPORT_STATIONS_FILE = RAW_DATA_DIR / "transport_stations.csv"
SYNTHETIC_EMPLOYEES_FILE = SYNTHETIC_DATA_DIR / "synthetic_employees.csv"
COMMUTE_FEATURES_FILE = PROCESSED_DATA_DIR / "employee_commute_features.csv"
ADOPTION_OUTPUT_FILE = PROCESSED_DATA_DIR / "adoption_scoring_output.csv"
POWERBI_OUTPUT_FILE = PROCESSED_DATA_DIR / "powerbi_dashboard_data.csv"