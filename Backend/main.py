from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "Hospital reccomendations API"}

# @app.get("/hospital")
# def hospital():
#     return {
#         "name" : "AIIMS Bhopal",
#         "rating" : 4.6
#     }

@app.get("/hospital")
def get_hospital(id: int):
    return {
        "hospital_id" : id,
        "name" : "Hospital" + str(id)
    }

@app.get("/recommend")
def recommend(service: str, city: str):
    return {
        "service" : service,
        "city" : city
    }

@app.post("/hospital-score")
def calc_score(cardiology_rating: float, icu_beds: int):
    score = cardiology_rating * icu_beds
    return {"score" : score}
