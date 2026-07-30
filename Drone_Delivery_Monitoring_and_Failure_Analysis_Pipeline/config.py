from pathlib import Path

# ==========================
# PROJECT PATHS
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parent

RAW_DATA_DIR = PROJECT_ROOT / "raw_data"
DOCUMENTS_DIR = PROJECT_ROOT / "documents"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
WORKFLOW_DIR = PROJECT_ROOT / "workflow"

# ==========================
# DATA FILES
# ==========================

DELIVERIES_FILE = RAW_DATA_DIR / "deliveries.csv"
DRONES_FILE = RAW_DATA_DIR / "drones.csv"
DRONE_UPDATES_FILE = RAW_DATA_DIR / "drones_update.csv"
FLIGHT_LOGS_FILE = RAW_DATA_DIR / "flight_logs.csv"

# ==========================
# DATA LAYERS
# ==========================

BRONZE_DIR = PROJECT_ROOT / "bronze"
SILVER_DIR = PROJECT_ROOT / "silver"
GOLD_DIR = PROJECT_ROOT / "gold"

# ==========================
# CREATE PROJECT DIRECTORIES
# ==========================

for directory in [BRONZE_DIR, SILVER_DIR, GOLD_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
    
# ==========================
# BUSINESS RULES
# ==========================

BATTERY_THRESHOLD = 20.0
SIGNAL_THRESHOLD = 0.30

WEATHER_FAIL_CONDITIONS = [
    "heavy rain",
    "storm"
]