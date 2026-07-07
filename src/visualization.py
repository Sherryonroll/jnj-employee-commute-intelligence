import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import ADOPTION_OUTPUT_FILE, CHARTS_DIR, SUMMARY_DIR


COMMUTE_ORDER = ["0-30 min", "31-45 min", "46-60 min", "60+ min"]
ADOPTION_ORDER = ["Low", "Medium", "High", "Very High"]


def save_bar_chart(data, x, y, title, xlabel, ylabel, filename, order=None):
    plt.figure(figsize=(9, 5))
    sns.barplot(data=data, x=x, y=y, order=order, color="#2F80ED")

    plt.title(title, fontsize=14, weight="bold")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    plt.savefig(CHARTS_DIR / filename, dpi=300)
    plt.close()


def plot_commute_group_distribution(df):
    commute_counts = (
        df["base_commute_group"]
        .value_counts(normalize=True)
        .mul(100)
        .reindex(COMMUTE_ORDER)
        .reset_index()
    )
    commute_counts.columns = ["commute_group", "percentage"]

    save_bar_chart(
        data=commute_counts,
        x="commute_group",
        y="percentage",
        title="Base Commute Time Distribution",
        xlabel="Commute Time Group",
        ylabel="Employees (%)",
        filename="commute_group_distribution.png",
        order=COMMUTE_ORDER,
    )


def plot_base_vs_delay_commute(df):
    comparison_df = pd.DataFrame(
        {
            "Base commute": df["base_commute_group"].value_counts(normalize=True).mul(100),
            "Delay-adjusted commute": df["risk_adjusted_commute_group"]
            .value_counts(normalize=True)
            .mul(100),
        }
    ).reindex(COMMUTE_ORDER)

    comparison_df = comparison_df.reset_index().melt(
        id_vars="index",
        var_name="scenario",
        value_name="percentage",
    )
    comparison_df = comparison_df.rename(columns={"index": "commute_group"})

    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=comparison_df,
        x="commute_group",
        y="percentage",
        hue="scenario",
        order=COMMUTE_ORDER,
        palette=["#2F80ED", "#F2994A"],
    )

    plt.title("Commute Groups Before and After 15-Minute Delay Buffer", fontsize=14, weight="bold")
    plt.xlabel("Commute Time Group")
    plt.ylabel("Employees (%)")
    plt.legend(title="")
    plt.tight_layout()

    plt.savefig(CHARTS_DIR / "base_vs_delay_commute_groups.png", dpi=300)
    plt.close()


def plot_adoption_potential(df):
    adoption_counts = (
        df["adoption_potential"]
        .value_counts(normalize=True)
        .mul(100)
        .reindex(ADOPTION_ORDER)
        .fillna(0)
        .reset_index()
    )
    adoption_counts.columns = ["adoption_potential", "percentage"]

    save_bar_chart(
        data=adoption_counts,
        x="adoption_potential",
        y="percentage",
        title="Deutschlandticket Adoption Potential",
        xlabel="Adoption Potential",
        ylabel="Employees (%)",
        filename="adoption_potential_distribution.png",
        order=ADOPTION_ORDER,
    )


def plot_delay_impact(df):
    delay_counts = (
        df["delay_impact"]
        .value_counts(normalize=True)
        .mul(100)
        .reset_index()
    )
    delay_counts.columns = ["delay_impact", "percentage"]

    save_bar_chart(
        data=delay_counts,
        x="delay_impact",
        y="percentage",
        title="Delay Sensitivity Impact",
        xlabel="Delay Impact Category",
        ylabel="Employees (%)",
        filename="delay_impact_distribution.png",
    )


def plot_area_adoption_scores(df):
    area_scores = (
        df.groupby("home_area")["adoption_score"]
        .mean()
        .sort_values(ascending=True)
        .reset_index()
    )

    plt.figure(figsize=(9, 7))
    sns.barplot(
        data=area_scores,
        x="adoption_score",
        y="home_area",
        color="#27AE60",
    )

    plt.title("Average Adoption Score by Home Area", fontsize=14, weight="bold")
    plt.xlabel("Average Adoption Score")
    plt.ylabel("Home Area")
    plt.tight_layout()

    plt.savefig(CHARTS_DIR / "average_adoption_score_by_area.png", dpi=300)
    plt.close()


def plot_key_factor_correlations():
    correlation_file = SUMMARY_DIR / "key_factor_correlations.csv"
    correlations = pd.read_csv(correlation_file)

    plt.figure(figsize=(9, 5))
    sns.barplot(
        data=correlations,
        x="correlation_with_adoption_score",
        y="factor",
        color="#9B51E0",
    )

    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Key Factors Influencing Adoption Score", fontsize=14, weight="bold")
    plt.xlabel("Correlation with Adoption Score")
    plt.ylabel("Factor")
    plt.tight_layout()

    plt.savefig(CHARTS_DIR / "key_factor_correlations.png", dpi=300)
    plt.close()


def main():
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(ADOPTION_OUTPUT_FILE)

    sns.set_theme(style="whitegrid")

    plot_commute_group_distribution(df)
    plot_base_vs_delay_commute(df)
    plot_adoption_potential(df)
    plot_delay_impact(df)
    plot_area_adoption_scores(df)
    plot_key_factor_correlations()

    print(f"Charts created in: {CHARTS_DIR}")


if __name__ == "__main__":
    main()