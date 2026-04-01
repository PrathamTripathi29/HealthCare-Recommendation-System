from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import math

class HospitalQuery(BaseModel):
    latitude: float
    longitude: float
    service: str = "general"
    max_distance: float = 10
    top_n: int = 5

def compute_distance(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat/2)**2 + 
        math.cos(math.radians(lat1)) * 
        math.cos(math.radians(lat2)) * 
        math.sin(dlon/2)**2
    )

    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

app = FastAPI()

dataset = None

@app.on_event("startup")
def load_data():
    global dataset
    dataset = pd.read_csv("data/bhopal_final.csv")
    print("Dataset loaded: ", len(dataset))

@app.post("/recommend")
def recommend(query: HospitalQuery):

    df = dataset.copy()

    df["distance"] = df.apply(
        lambda row: compute_distance(
            query.latitude,
            query.longitude,
            row["latitude"],
            row["longitude"],
        ),
        axis = 1,
    )

    df = df[df["distance"] <= query.max_distance]

    baseline_score_col = (
        "rule_score_overall" if "rule_score_overall" in df.columns else "score"
    )
    # Distance penalty keeps relevance to the user location.
    df["final_score"] = df[baseline_score_col] - 0.05 * df["distance"]


    df = df.sort_values("final_score", ascending=False)

    df = df.head(query.top_n)

    response_columns =[
        "name",
        "latitude",
        "longitude",
        baseline_score_col,
        "distance",
        "final_score",
    ]

    phase_a_columns = [
        "rule_socre_feature_quality",
        "rule_score_feature_capacity",
        "rule_score_feature_affordability",
        "rule_score_feature_specialty",
    ]

    response_columns.extend([col for col in phase_a_columns if col in df.columns])
    return df[response_columns].to_dict(orient="records")
