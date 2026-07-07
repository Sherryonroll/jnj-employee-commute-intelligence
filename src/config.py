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

# Walking speed assumption
WALKING_SPEED_KMH = 4.8

# Public transport access thresholds
STATION_ACCESS_THRESHOLDS_M = {
    "excellent": 500,
    "good": 1000,
    "acceptable": 1500,
}

# Transfer assumptions
TRANSFER_PENALTY_MIN = 7

# Output files
SYNTHETIC_EMPLOYEES_FILE = SYNTHETIC_DATA_DIR / "synthetic_employees.csv"
COMMUTE_FEATURES_FILE = PROCESSED_DATA_DIR / "employee_commute_features.csv"
ADOPTION_OUTPUT_FILE = PROCESSED_DATA_DIR / "adoption_scoring_output.csv"
POWERBI_OUTPUT_FILE = PROCESSED_DATA_DIR / "powerbi_dashboard_data.csv"