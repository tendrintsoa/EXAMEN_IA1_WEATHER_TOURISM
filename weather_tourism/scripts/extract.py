import requests
import pandas as pd
from datetime import datetime

# Configuration API
API_KEY = "534b4c30c9337ee3686a1c15a7256639"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

cities = {
    "Paris": {"lat": 48.8566, "lon": 2.3522},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503},
    "Rio de Janeiro": {"lat": -22.9068, "lon": -43.1729},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "Sydney": {"lat": -33.8688, "lon": 151.2093}
}

def fetch_current_weather(city_name, lat, lon):
    """Récupère les données météo actuelles via l'API OpenWeather"""
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            'city': city_name,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'weather_description': data['weather'][0]['description'],
            'visibility': data.get('visibility', 0) / 1000  # Convert to km
        }
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données pour {city_name}: {e}")
        return None

def extract_data():
    """Extraction des données via OpenWeather API"""
    weather_data = []
    
    for city_name, coords in cities.items():
        print(f"Collecte des données pour {city_name}...")
        data = fetch_current_weather(city_name, coords['lat'], coords['lon'])
        if data:
            weather_data.append(data)
    
    df = pd.DataFrame(weather_data)
    df.to_csv('/home/hervino/airflow/dags/weather_tourism_project/data/current_weather.csv', index=False)
    
    print(f"Extracted {len(weather_data)} weather records")

if __name__ == "__main__":
    extract_data()


