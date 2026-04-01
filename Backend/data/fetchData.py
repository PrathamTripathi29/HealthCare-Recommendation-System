import requests
import pandas as pd

url = "https://overpass.kumi.systems/api/interpreter"

query = """
[out:json][timeout:25];
area["name"="Bhopal"]["boundary"="administrative"]->.searchArea;
(
  node["amenity"="hospital"](area.searchArea);
  node["amenity"="clinic"](area.searchArea);
);
out body;
"""

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, params={"data": query}, headers=headers)

if response.status_code != 200:
    print("Error:", response.text)
    exit()

data = response.json()

hospitals = []

for el in data["elements"]:
    name = el.get("tags", {}).get("name", "Unknown")

    hospitals.append({
        "name": name,
        "latitude": el.get("lat"),
        "longitude": el.get("lon")
    })

df = pd.DataFrame(hospitals)

df.to_csv("data/bhopal_raw.csv", index=False)

print("Raw data saved:", len(df))