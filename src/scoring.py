import pandas as pd

from config import COMMUTE_FEATURES_FILE, ADOPTION_OUTPUT_FILE, POWERBI_OUTPUT_FILE


def commute_time_score(minutes):
    if minutes <= 30:
        return 35
    if minutes <= 45:
        return 28
    if minutes <= 60:
        return 18
    return 8


def station_access_score(distance_m):
    if distance_m <= 500:
        return 25
    if distance_m <= 1000:
        return 18
    if distance_m <= 1500:
        return 10
    return 4


def transfer_score(number_of_transfers):
    if number_of_transfers == 0:
        return 20
    if number_of_transfers == 1:
        return 14
    if number_of_transfers == 2:
        return 8
    return 3


def reliability_score(delay_impact):
    if delay_impact == "No impact":
        return 20
    if delay_impact == "Minor impact":
        return 10
    return 3


def classify_adoption_potential(score):
    if score >= 80:
        return "Very High"
    if score >= 65:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def calculate_adoption_scores(commute_df):
    scored_df = commute_df.copy()

    scored_df["commute_time_score"] = scored_df["base_commute_time_min"].apply(
        commute_time_score
    )
    scored_df["station_access_score"] = scored_df["home_to_station_m"].apply(
        station_access_score
    )
    scored_df["transfer_score"] = scored_df["number_of_transfers"].apply(
        transfer_score
    )
    scored_df["reliability_score"] = scored_df["delay_impact"].apply(
        reliability_score
    )

    scored_df["adoption_score"] = (
        scored_df["commute_time_score"]
        + scored_df["station_access_score"]
        + scored_df["transfer_score"]
        + scored_df["reliability_score"]
    )

    scored_df["adoption_potential"] = scored_df["adoption_score"].apply(
        classify_adoption_potential
    )

    return scored_df


def main():
    commute_df = pd.read_csv(COMMUTE_FEATURES_FILE)

    ADOPTION_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    scored_df = calculate_adoption_scores(commute_df)

    scored_df.to_csv(ADOPTION_OUTPUT_FILE, index=False)
    scored_df.to_csv(POWERBI_OUTPUT_FILE, index=False)

    print(f"Adoption scoring output created: {ADOPTION_OUTPUT_FILE}")
    print(f"Power BI-ready dataset created: {POWERBI_OUTPUT_FILE}")

    print("\nAdoption potential distribution:")
    print(scored_df["adoption_potential"].value_counts(normalize=True).mul(100).round(1))

    print("\nAverage adoption score by area:")
    print(
        scored_df.groupby("home_area")["adoption_score"]
        .mean()
        .sort_values(ascending=False)
        .round(1)
    )

    print("\nSample rows:")
    print(
        scored_df[
            [
                "employee_id",
                "home_area",
                "base_commute_time_min",
                "risk_adjusted_commute_time_min",
                "home_to_station_m",
                "number_of_transfers",
                "delay_impact",
                "adoption_score",
                "adoption_potential",
            ]
        ].head()
    )


if __name__ == "__main__":
    main()