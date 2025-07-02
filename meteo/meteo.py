import requests
import json
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PARIS_LAT = 48.85
PARIS_LON = 2.35
API_URL = "https://archive-api.open-meteo.com/v1/archive"


def get_weather_data():
    """Récupère les données météo de l'API"""
    params = {
        "latitude": PARIS_LAT,
        "longitude": PARIS_LON,
        "start_date": "2025-06-24",
        "end_date": "2025-06-30",
        "hourly": "temperature_2m"
    }
    
    try: 
        response = requests.get(API_URL, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Erreur lors de la récupération des données météo: {response.status_code}")
            
        return response.json()
    
    except requests.RequestException as e:
        raise Exception(f"Erreur lors de la récupération des données météo: {str(e)}")


def analyze_weather_by_day(data):
    """Analyse les données météo et calcule des statistiques par jour"""
    if "hourly" not in data or "temperature_2m" not in data["hourly"]:
        raise ValueError("Données météo manquantes")
    
    times = data["hourly"]["time"]
    temperatures = data["hourly"]["temperature_2m"]
    
    if not times or not temperatures:
        raise ValueError("Aucune donnée de température")
    
    # Grouper les températures par jour
    daily_temps = defaultdict(list)
    
    for time_str, temp in zip(times, temperatures):
        # Extraire la date (YYYY-MM-DD) du timestamp
        date = time_str.split('T')[0]
        daily_temps[date].append(temp)
    
    # Calculer les statistiques par jour
    jours = []
    all_temps = []
    
    for date in sorted(daily_temps.keys()):
        temps = daily_temps[date]
        jour_stats = {
            "date": date,
            "temperature_moyenne": round(sum(temps) / len(temps), 1),
            "temperature_min": round(min(temps), 1),
            "temperature_max": round(max(temps), 1),
            "nombre_mesures": len(temps)
        }
        jours.append(jour_stats)
        all_temps.extend(temps)
    
    # Statistiques sur toute la période
    periode_stats = {
        "temperature_moyenne_totale": round(sum(all_temps) / len(all_temps), 1),
        "temperature_min_totale": round(min(all_temps), 1),
        "temperature_max_totale": round(max(all_temps), 1),
        "nombre_jours": len(jours),
        "date_debut": jours[0]["date"],
        "date_fin": jours[-1]["date"]
    }
    
    return {
        "jours": jours,
        "periode": periode_stats
    }


def save_results(results, filepath="meteo.json"):
    """Sauvegarde les résultats dans un fichier JSON"""
    data_to_save = {
        "timestamp": datetime.now().isoformat(),
        "localisation": {
            "latitude": PARIS_LAT,
            "longitude": PARIS_LON,
            "ville": "Paris"
        },
        "resultats": results
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)


def afficher_rapport(analysis):
    """Affiche un rapport formaté des résultats"""
    print("\n" + "="*60)
    print(f"📍 ANALYSE MÉTÉO PARIS - {analysis['periode']['date_debut']} au {analysis['periode']['date_fin']}")
    print("="*60)
    
    print(f"\n📊 Résumé sur {analysis['periode']['nombre_jours']} jours:")
    print(f"   • Température moyenne: {analysis['periode']['temperature_moyenne_totale']}°C")
    print(f"   • Température min: {analysis['periode']['temperature_min_totale']}°C")
    print(f"   • Température max: {analysis['periode']['temperature_max_totale']}°C")
    
    print("\n📅 Détails par jour:")
    for jour in analysis['jours']:
        print(f"\n   {jour['date']}:")
        print(f"   • Moyenne: {jour['temperature_moyenne']}°C")
        print(f"   • Min: {jour['temperature_min']}°C / Max: {jour['temperature_max']}°C")


def create_temperature_graph(analysis):
    """Crée un graphique des températures moyennes par jour"""
    if not analysis.get('jours'):
        raise ValueError("Aucune donnée de température à afficher")
    
    # Extraire les données
    dates = []
    temperatures = []
    
    for jour in analysis['jours']:
        # Convertir la date string en objet datetime
        date_obj = datetime.strptime(jour['date'], '%Y-%m-%d')
        dates.append(date_obj)
        temperatures.append(jour['temperature_moyenne'])
    
    # Créer le graphique
    plt.figure(figsize=(12, 6))
    
    # Graphique en ligne avec marqueurs
    plt.plot(dates, temperatures, 'b-o', linewidth=2, markersize=8, label='Température moyenne')
    
    # Ajouter la ligne de moyenne totale
    if 'periode' in analysis and 'temperature_moyenne_totale' in analysis['periode']:
        moyenne_totale = analysis['periode']['temperature_moyenne_totale']
        plt.axhline(y=moyenne_totale, color='r', linestyle='--', alpha=0.7, 
                   label=f'Moyenne période: {moyenne_totale}°C')
    
    # Personnalisation
    plt.title('Températures moyennes à Paris - 7 derniers jours', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Température (°C)', fontsize=12)
    
    # Formatter les dates sur l'axe x
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)
    
    # Ajouter une grille
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Ajouter les valeurs sur les points
    for date, temp in zip(dates, temperatures):
        plt.annotate(f'{temp}°C', 
                    (date, temp), 
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center',
                    fontsize=10)
    
    # Légende
    plt.legend(loc='best')
    
    # Ajuster la mise en page
    plt.tight_layout()
    
    # Sauvegarder et afficher
    plt.savefig('temperatures_paris.png', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    print("🌤️  Récupération des données météo...")
    try:
        data = get_weather_data()
        
        print("📊 Analyse des données...")
        results = analyze_weather_by_day(data)
        
        afficher_rapport(results)
        
        save_results(results)
        print("\n💾 Résultats sauvegardés dans meteo.json")
        
        print("\n📈 Création du graphique...")
        create_temperature_graph(results)
        print("📈 Graphique sauvegardé dans temperatures_paris.png")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")