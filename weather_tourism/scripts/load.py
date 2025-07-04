import pandas as pd
import sqlite3
from datetime import datetime
import json

def load_data():
    """Chargement des données dans la base de données et génération des recommandations"""
    # Chargement des données transformées
    df = pd.read_csv("/home/hervino/airflow/dags/weather_tourism_project/data/weather_combined.csv")
    
    # Connexion à la base de données
    conn = sqlite3.connect("/home/hervino/airflow/dags/weather_tourism_project/data/weather_tourism.db")
    
    # Chargement dans la table principale
    df.to_sql("weather_tourism_data", conn, if_exists="replace", index=False)
    
    # Création d"une vue pour les recommandations
    cursor = conn.cursor()
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS tourism_recommendations AS
        SELECT 
            city,
            AVG(tourism_score) as avg_score,
            AVG(temperature) as avg_temp,
            AVG(humidity) as avg_humidity,
            COUNT(*) as data_points
        FROM weather_tourism_data
        GROUP BY city
        ORDER BY avg_score DESC
    """)
    
    conn.commit()
    
    # Requête pour les meilleures recommandations
    query = """
        SELECT city, avg_score, avg_temp, avg_humidity
        FROM tourism_recommendations
        WHERE avg_score >= 70
        ORDER BY avg_score DESC
    """
    
    recommendations_df = pd.read_sql_query(query, conn)
    
    # Génération du rapport JSON
    recommendations = {
        "generated_at": datetime.now().isoformat(),
        "top_destinations": recommendations_df.to_dict("records"),
        "summary": {
            "total_cities_analyzed": len(recommendations_df),
            "best_destination": recommendations_df.iloc[0]["city"] if len(recommendations_df) > 0 else None
        }
    }
    
    # Sauvegarde du rapport
    with open("/home/hervino/airflow/dags/weather_tourism_project/data/tourism_recommendations.json", "w") as f:
        json.dump(recommendations, f, indent=2)
    
    conn.close()
    
    print(f"Loaded {len(df)} records to database and generated recommendations for {len(recommendations_df)} cities")

if __name__ == "__main__":
    load_data()

