import pandas as pd

from config import ADOPTION_OUTPUT_FILE, SUMMARY_DIR


def percentage_table(series):
    return (
        series.value_counts(normalize=True)
        .mul(100)
        .round(1)
        .reset_index()
        .rename(columns={"index": "category", series.name: "percentage"})
    )


def create_area_summary(df):
    area_summary = (
        df.groupby("home_area")
        .agg(
            employees=("employee_id", "count"),
            avg_base_commute_min=("base_commute_time_min", "mean"),
            avg_delay_adjusted_commute_min=("risk_adjusted_commute_time_min", "mean"),
            avg_public_transport_access_m=("nearest_public_transport_access_m", "mean"),
            avg_transfers=("number_of_transfers", "mean"),
            avg_adoption_score=("adoption_score", "mean"),
            high_or_very_high_potential=(
                "adoption_potential",
                lambda x: x.isin(["High", "Very High"]).mean() * 100,
            ),
        )
        .round(1)
        .reset_index()
        .sort_values("avg_adoption_score", ascending=False)
    )

    return area_summary


def create_key_factor_summary(df):
    factor_columns = [
        "base_commute_time_min",
        "risk_adjusted_commute_time_min",
        "nearest_public_transport_access_m",
        "number_of_transfers",
        "station_connectivity_score",
    ]

    correlations = (
        df[factor_columns + ["adoption_score"]]
        .corr(numeric_only=True)["adoption_score"]
        .drop("adoption_score")
        .sort_values()
        .round(3)
        .reset_index()
    )

    correlations.columns = ["factor", "correlation_with_adoption_score"]
    return correlations


def create_executive_summary(df):
    total_employees = len(df)

    under_30 = (df["base_commute_time_min"] <= 30).mean() * 100
    under_45 = (df["base_commute_time_min"] <= 45).mean() * 100
    under_60 = (df["base_commute_time_min"] <= 60).mean() * 100
    over_60 = (df["base_commute_time_min"] > 60).mean() * 100

    high_potential = df["adoption_potential"].isin(["High", "Very High"]).mean() * 100
    delay_sensitive = (df["delay_impact"] != "No impact").mean() * 100
    crosses_45_after_delay = df["crosses_45_min_after_delay"].mean() * 100

    summary = pd.DataFrame(
        {
            "metric": [
                "Total synthetic employees",
                "Employees within 30 minutes",
                "Employees within 45 minutes",
                "Employees within 60 minutes",
                "Employees over 60 minutes",
                "High or very high adoption potential",
                "Delay-sensitive employees",
                "Employees crossing 45 minutes after delay",
                "Average base commute time",
                "Average delay-adjusted commute time",
                "Average adoption score",
            ],
            "value": [
                total_employees,
                round(under_30, 1),
                round(under_45, 1),
                round(under_60, 1),
                round(over_60, 1),
                round(high_potential, 1),
                round(delay_sensitive, 1),
                round(crosses_45_after_delay, 1),
                round(df["base_commute_time_min"].mean(), 1),
                round(df["risk_adjusted_commute_time_min"].mean(), 1),
                round(df["adoption_score"].mean(), 1),
            ],
        }
    )

    return summary


def main():
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(ADOPTION_OUTPUT_FILE)

    executive_summary = create_executive_summary(df)
    area_summary = create_area_summary(df)
    key_factors = create_key_factor_summary(df)

    executive_summary.to_csv(SUMMARY_DIR / "executive_summary.csv", index=False)
    area_summary.to_csv(SUMMARY_DIR / "area_connectivity_summary.csv", index=False)
    key_factors.to_csv(SUMMARY_DIR / "key_factor_correlations.csv", index=False)

    print("Summary files created successfully.")
    print("\nExecutive summary:")
    print(executive_summary)

    print("\nTop connected areas:")
    print(area_summary.head(5))

    print("\nLower attractiveness areas:")
    print(area_summary.tail(5))

    print("\nKey factor correlations:")
    print(key_factors)


if __name__ == "__main__":
    main()