import pandas as pd

def transform_data():
    """Transformation et nettoyage des données"""
    # Chargement des données actuelles
    current_df = pd.read_csv("/home/hervino/airflow/dags/weather_tourism_project/data/current_weather.csv")
    
    # Chargement des données historiques
    # Note: Dans un vrai scénario, vous auriez une source de données historiques plus robuste
    # Pour cet exemple, nous allons simuler des données historiques ou utiliser celles déjà générées
    try:
        historical_df = pd.read_csv("/home/hervino/airflow/dags/weather_tourism_project/data/weather_with_scores.csv")
    except FileNotFoundError:
        print("Fichier historical_weather_data.csv non trouvé. Création d\"un DataFrame vide.")
        historical_df = pd.DataFrame(columns=[
            "city", "date", "temperature", "humidity", "pressure", "wind_speed", 
            "weather_description", "tourism_score"
        ])

    # Calcul du score de tourisme pour les données actuelles
    def calculate_tourism_score(row):
        temp_score = 100 if 22 <= row["temperature"] <= 28 else max(0, 100 - abs(row["temperature"] - 25) * 4)
        humidity_score = 100 if 40 <= row["humidity"] <= 60 else max(0, 100 - abs(row["humidity"] - 50) * 2)
        wind_score = 100 if row["wind_speed"] <= 20 else max(0, 100 - (row["wind_speed"] - 20) * 3)
        
        return int((temp_score + humidity_score + wind_score) / 3)
    
    current_df["tourism_score"] = current_df.apply(calculate_tourism_score, axis=1)
    
    # Fusion avec les données historiques
    combined_df = pd.concat([historical_df, current_df], ignore_index=True)
    
    # Sauvegarde des données transformées
    combined_df.to_csv("/home/hervino/airflow/dags/weather_tourism_project/data/weather_combined.csv", index=False)
    
    print(f"Transformed and combined {len(combined_df)} total records")

if __name__ == "__main__":
    transform_data()

