import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from config import ADOPTION_OUTPUT_FILE, POWERBI_OUTPUT_FILE


FEATURE_COLUMNS = [
    "base_commute_time_min",
    "risk_adjusted_commute_time_min",
    "home_to_station_m",
    "number_of_transfers",
    "station_connectivity_score",
    "adoption_score",
]


def assign_segment_name(row):
    if row["adoption_score"] >= 80 and row["base_commute_time_min"] <= 45:
        return "High-potential PT users"

    if row["home_to_station_m"] > 1500:
        return "Poor station access commuters"

    if row["crosses_45_min_after_delay"]:
        return "Delay-sensitive commuters"

    if row["base_commute_time_min"] <= 60 and row["delay_impact"] != "No impact":
        return "Delay-sensitive commuters"

    if row["base_commute_time_min"] <= 75 and row["adoption_score"] >= 55:
        return "Moderate-potential commuters"

    if row["base_commute_time_min"] > 75:
        return "Long commute commuters"

    return "Moderate-potential commuters"


def add_commuter_segments(scored_df, n_clusters=4):
    segmented_df = scored_df.copy()

    X = segmented_df[FEATURE_COLUMNS].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    segmented_df["ml_cluster"] = kmeans.fit_predict(X_scaled)

    segmented_df["commuter_segment"] = segmented_df.apply(assign_segment_name, axis=1)

    return segmented_df


def main():
    scored_df = pd.read_csv(ADOPTION_OUTPUT_FILE)

    segmented_df = add_commuter_segments(scored_df)

    segmented_df.to_csv(ADOPTION_OUTPUT_FILE, index=False)
    segmented_df.to_csv(POWERBI_OUTPUT_FILE, index=False)

    print("Commuter segmentation added successfully.")
    print(f"Updated file: {ADOPTION_OUTPUT_FILE}")
    print(f"Updated Power BI file: {POWERBI_OUTPUT_FILE}")

    print("\nCommuter segment distribution:")
    print(
        segmented_df["commuter_segment"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
    )

    print("\nAverage values by commuter segment:")
    print(
        segmented_df.groupby("commuter_segment")[
            [
                "base_commute_time_min",
                "risk_adjusted_commute_time_min",
                "home_to_station_m",
                "number_of_transfers",
                "adoption_score",
            ]
        ]
        .mean()
        .round(1)
    )


if __name__ == "__main__":
    main()