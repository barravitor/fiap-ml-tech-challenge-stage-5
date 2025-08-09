
import time
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="fiap-ml-tech-challenge-stage-5")

def get_coordinates(location_text, retries=3):
    try:
        location = geolocator.geocode(location_text, timeout=3)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        if retries > 0:
            time.sleep(3)
            return get_coordinates(location_text, retries - 1)
    return None, None

def get_geo_distance(row):
    try:
        job_coords = (row['job_latitude'], row['job_longitude'])
        user_coords = (row['user_latitude'], row['user_longitude'])

        if pd.isnull(job_coords[0]) or pd.isnull(job_coords[1]) or pd.isnull(user_coords[0]) or pd.isnull(user_coords[1]):
            return None

        return geodesic(job_coords, user_coords).km
    except Exception:
        return None

def generate_geocodes(df: pd.DataFrame) -> pd.DataFrame :
    location_list = pd.concat([df['job_local'], df['user_local']]).dropna().loc[lambda x: x.str.strip() != ''].unique()

    locations = []
    for loc in location_list:
        print(loc)
        lat, lon = get_coordinates(loc)
        locations.append({
            'location': loc,
            'latitude': lat,
            'longitude': lon
        })

    return pd.DataFrame(locations)

