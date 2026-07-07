import pandas as pd

from config import SYNTHETIC_EMPLOYEES_FILE, VALIDATED_EMPLOYEES_FILE


EXPECTED_COLUMNS = [
    "employee_id",
    "home_area",
    "area_type",
    "latitude",
    "longitude",
]

VALID_AREA_TYPES = {
    "near_workplace",
    "urban",
    "outer_urban",
    "suburban",
    "outer_suburban",
    "regional",
}


def validate_required_columns(df):
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def validate_missing_values(df):
    missing_counts = df[EXPECTED_COLUMNS].isna().sum()
    total_missing = missing_counts.sum()

    if total_missing > 0:
        raise ValueError(f"Missing values found:\n{missing_counts[missing_counts > 0]}")


def validate_unique_employee_ids(df):
    duplicate_count = df["employee_id"].duplicated().sum()

    if duplicate_count > 0:
        raise ValueError(f"Duplicate employee IDs found: {duplicate_count}")


def validate_coordinate_ranges(df):
    invalid_coordinates = df[
        ~df["latitude"].between(53.15, 53.95)
        | ~df["longitude"].between(9.50, 10.50)
    ]

    if not invalid_coordinates.empty:
        raise ValueError(
            f"Coordinates outside expected Hamburg/Norderstedt region: "
            f"{len(invalid_coordinates)} rows"
        )


def validate_area_types(df):
    invalid_area_types = set(df["area_type"]) - VALID_AREA_TYPES

    if invalid_area_types:
        raise ValueError(f"Invalid area types found: {invalid_area_types}")


def clean_employee_data(df):
    cleaned_df = df.copy()

    cleaned_df["employee_id"] = cleaned_df["employee_id"].astype(str).str.strip()
    cleaned_df["home_area"] = cleaned_df["home_area"].astype(str).str.strip()
    cleaned_df["area_type"] = cleaned_df["area_type"].astype(str).str.strip()

    cleaned_df["latitude"] = cleaned_df["latitude"].astype(float)
    cleaned_df["longitude"] = cleaned_df["longitude"].astype(float)

    return cleaned_df


def preprocess_employee_data(df):
    validate_required_columns(df)

    cleaned_df = clean_employee_data(df)

    validate_missing_values(cleaned_df)
    validate_unique_employee_ids(cleaned_df)
    validate_coordinate_ranges(cleaned_df)
    validate_area_types(cleaned_df)

    return cleaned_df


def main():
    employees_df = pd.read_csv(SYNTHETIC_EMPLOYEES_FILE)

    VALIDATED_EMPLOYEES_FILE.parent.mkdir(parents=True, exist_ok=True)

    validated_df = preprocess_employee_data(employees_df)
    validated_df.to_csv(VALIDATED_EMPLOYEES_FILE, index=False)

    print(f"Validated employee dataset created: {VALIDATED_EMPLOYEES_FILE}")
    print(f"Number of validated employees: {len(validated_df)}")
    print("\nArea type distribution:")
    print(validated_df["area_type"].value_counts())


if __name__ == "__main__":
    main()