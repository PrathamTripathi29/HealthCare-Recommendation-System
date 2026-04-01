import pandas as pd
import random

df = pd.read_csv("data/bhopal_raw.csv")
print("Original size:", len(df))

df = df[df["name"] != "Unknown"]

df = df.drop_duplicates(subset=["name"])

df = df.dropna(subset=["latitude", "longitude"])

print("Cleaned size: ", len(df))

df["cardiology_rating"] = [round(random.uniform(2, 5), 2) for _ in range(len(df))]
df["orthopedic_rating"] = [round(random.uniform(2,5),2) for _ in range(len(df))]
df["icu_beds"] = [random.randint(5,50) for _ in range(len(df))]
df["emergency_services"] = [random.choice([0,1]) for _ in range(len(df))]
df["doctor_experience"] = [round(random.uniform(2,5),2) for _ in range(len(df))]
df["patient_satisfaction"] = [round(random.uniform(2,5),2) for _ in range(len(df))]
df["cost_index"] = [random.randint(1,5) for _ in range(len(df))]

df["score"] = (
    0.4 * df["cardiology_rating"] + 
    0.3 * df["patient_satisfaction"] + 
    0.2 * df["doctor_experience"] + 
    0.1 * (df["icu_beds"] / 50)
)

df = df.sort_values("score", ascending=False)

df.to_csv("data/bhopal_final.csv", index = False)

print("Final dataset saved: ", len(df))