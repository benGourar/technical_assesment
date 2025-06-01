
import requests
import sqlite3
import time
import logging
from typing import Optional, List, Dict
import os

print("Current working directory:", os.getcwd())


# establishing connection using API_KEY
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

API_KEY = "92ad2cb15b5e9fa06d1635b8713c7f611ee3d7b0577c49d51cfe9f9c2e50c6cc"
BASE_URL = "https://api.openaq.org/v3/locations/"

#Searching for location in OpenAQ dataset

def location_search(location_id: int, retries: int = 3, delay: int = 3) -> Optional[dict]:
    url = f"{BASE_URL}{location_id}"
    headers = {"X-API-Key": API_KEY}

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if "results" in data and data["results"]:
                return data["results"][0]
            else:
                logging.warning(f"No results found for location {location_id}")
                return None
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                logging.warning(f"Rate limit reached. Retrying in {delay} seconds...")
                time.sleep(5)
            else:
                logging.error(f"HTTP error for location {location_id}: {e}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error for location {location_id}: {e}")
            return None
    return None


#Retrieving good Data and Bad Data
def clean_location_data(data):
    return {
        "id": data.get("id"),
        "name": data.get("name") or "Unnamed",
        "locality": data.get("locality") or "Unknown",
        "timezone": data.get("timezone") or "Unknown",
        "country_code": data.get("country", {}).get("code", "XX") if data.get("country") else "XX",
        "country_name": data.get("country", {}).get("name", "Unknown") if data.get("country") else "Unknown",
        "provider": data["provider"]["name"] if data.get("provider") and isinstance(data["provider"], dict) else "Unknown",
        "latitude": data.get("coordinates", {}).get("latitude"),
        "longitude": data.get("coordinates", {}).get("longitude")
    }


#Cleaning the bad sensors data
def clean_sensors_data(sensors: List[dict], location_id: int) -> List[Dict]:
    cleaned = []
    for sensor in sensors:
        param = sensor.get("parameter", {})
        cleaned.append({
            "sensor_id": sensor.get("id"),
            "location_id": location_id,
            "param_name": param.get("name", "unknown").lower(),
            "display_name": param.get("displayName", "").upper(),
            "unit": param.get("units", "unknown")
        })
    return cleaned

#Starting SQL connection and bulding database
def initialize_db():
    conn = sqlite3.connect("openaq_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS location (
            id INTEGER PRIMARY KEY,
            name TEXT,
            locality TEXT,
            timezone TEXT,
            country_code TEXT,
            country_name TEXT,
            provider TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor (
            sensor_id INTEGER PRIMARY KEY,
            location_id INTEGER,
            param_name TEXT,
            display_name TEXT,
            unit TEXT,
            FOREIGN KEY(location_id) REFERENCES location(id)
        )
    """)

    conn.commit()
    conn.close()

#Inserting data after ETL process

def insert_into_db(location: dict, sensors: List[dict]):
    conn = sqlite3.connect("openaq_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO location 
        (id, name, locality, timezone, country_code, country_name, provider, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        location["id"], location["name"], location["locality"], location["timezone"],
        location["country_code"], location["country_name"], location["provider"],
        location["latitude"], location["longitude"]
    ))

    for sensor in sensors:
        cursor.execute("""
            INSERT OR REPLACE INTO sensor 
            (sensor_id, location_id, param_name, display_name, unit)
            VALUES (?, ?, ?, ?, ?)
        """, (
            sensor["sensor_id"], sensor["location_id"], sensor["param_name"],
            sensor["display_name"], sensor["unit"]
        ))

    conn.commit()
    conn.close()

#Running the etl process on data
def run_etl(location_ids: List[int], test_mode: bool = False):
    initialize_db()

    for loc_id in location_ids:
        logging.info(f"Processing location ID: {loc_id}")

        if test_mode:
            import json
            with open("test_data.json") as f:
                raw = json.load(f)["results"][0]
        else:
            raw = location_search(loc_id)

        if not raw:
            logging.warning(f"Skipping location {loc_id} due to fetch failure.")
            continue

        location_data = clean_location_data(raw)
        sensor_data = clean_sensors_data(raw.get("sensors", []), location_id=loc_id)

        insert_into_db(location_data, sensor_data)
        logging.info(f"Location {loc_id} processed.")

    logging.info("ETL completed for all locations.")


if __name__ == "__main__":
    location_ids = [2178]
    run_etl(location_ids, test_mode=True)
