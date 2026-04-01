import pandas as pd
import random

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

#weights for score families
QUALITY_WEIGHT = 0.50
CAPACITY_WEIGHT = 0.25
AFFORDABILITY_WEIGHT = 0.15
SPECIALTY_WEIGHT = 0.10

def minmax_normalize(series: pd.Series, floor: float, ceiling: float) -> pd.Series:
    """normalizing values from 0-1"""
    return (series - floor)/(ceiling - floor)

def build_phase_a_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Creating rule-based feature family scores and overall baseline score"""
    cardio_norm = minmax_normalize(df["cardiology_rating"], 2, 5)
    ortho_norm = minmax_normalize(df["orthopedic_rating"], 2, 5)
    doctor_exp_norm = minmax_normalize(df["doctor_experience"], 2, 5)
    patient_sat_norm = minmax_normalize(df["patient_satisfaction"], 2, 5)
    icu_norm = minmax_normalize(df["icu_beds"], 5, 50)
    cost_inverse_norm = 1 - minmax_normalize(df["cost_index"], 1, 5)

    #Feature family rule scores
    df["rule_score_feature_quality"] = (
        0.35 * cardio_norm
        + 0.15 * ortho_norm
        + 0.20 * doctor_exp_norm
        + 0.30 * patient_sat_norm
    )

    df["rule_score_feature_capacity"] = (
        0.70 * icu_norm + 0.30 * df["emergency_services"]
    )

    df["rule_score_feature_affordability"] = cost_inverse_norm

    df["rule_score_feature_specialty"] = (
        0.55 * cardio_norm + 0.45 * ortho_norm
    )

    # Aggregate baseline rule score (0-1), then project to 2-5 for compatibility.
    rule_score_0_to_1 = (
        QUALITY_WEIGHT * df["rule_score_feature_quality"]
        + CAPACITY_WEIGHT * df["rule_score_feature_capacity"]
        + AFFORDABILITY_WEIGHT * df["rule_score_feature_affordability"]
        + SPECIALTY_WEIGHT * df["rule_score_feature_specialty"]
    )

    df["rule_score_overall"] = 2 + 3 * rule_score_0_to_1

    # Backward compatibility with existing API logic.
    df["score"] = df["rule_score_overall"]

    return df


def main() -> None:
    df = pd.read_csv("data/bhopal_raw.csv")
    print("Original Size: ", len(df))

    df = df[df["name"] != "Unknown"]
    df = df.drop_duplicates(subset=["name"])
    df = df.dropna(subset=["latitude", "longitude"])
    print("Cleaned size:", len(df))

    df["cardiology_rating"] = [round(random.uniform(2, 5), 2) for _ in range(len(df))]
    df["orthopedic_rating"] = [round(random.uniform(2,5),2) for _ in range(len(df))]
    df["icu_beds"] = [random.randint(5,50) for _ in range(len(df))]
    df["emergency_services"] = [random.choice([0,1]) for _ in range(len(df))]
    df["doctor_experience"] = [round(random.uniform(2,5),2) for _ in range(len(df))]
    df["patient_satisfaction"] = [round(random.uniform(2,5),2) for _ in range(len(df))]
    df["cost_index"] = [random.randint(1,5) for _ in range(len(df))]
    df = build_phase_a_scores(df)
    df = df.sort_values("rule_score_overall", ascending=False)
    df.to_csv("data/bhopal_final.csv", index=False)
    print("Final dataset saved:", len(df))

if __name__ == "__main__":
    main()