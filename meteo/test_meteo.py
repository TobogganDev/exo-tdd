import pytest
import json
from unittest.mock import patch

from meteo import get_weather_data, analyze_weather_by_day, save_results, create_temperature_graph

def test_get_weather_data():
    """Test la récupération des données météo"""
    fake_response = {
        "hourly": {
            "time": ["2025-06-24T00:00", "2025-06-24T01:00"],
            "temperature_2m": [15.0, 16.0]
        }
    }
    
    with patch('meteo.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = fake_response
        
        data = get_weather_data()
        
        assert data == fake_response
        mock_get.assert_called_once()


def test_analyze_weather_by_day():
    """Test l'analyse des données par jour"""
    # Données de test avec 2 jours
    fake_data = {
        "hourly": {
            "time": [
                "2025-06-24T00:00", "2025-06-24T12:00", "2025-06-24T23:00",
                "2025-06-25T00:00", "2025-06-25T12:00", "2025-06-25T23:00"
            ],
            "temperature_2m": [15.0, 25.0, 20.0, 18.0, 30.0, 22.0]
        }
    }
    
    result = analyze_weather_by_day(fake_data)
    
    assert len(result["jours"]) == 2
    
    jour1 = result["jours"][0]
    assert jour1["date"] == "2025-06-24"
    assert jour1["temperature_moyenne"] == 20.0
    assert jour1["temperature_min"] == 15.0
    assert jour1["temperature_max"] == 25.0
    
    assert result["periode"]["temperature_moyenne_totale"] == pytest.approx(21.67, 0.01)


def test_save_results_by_day(tmp_path):
    """Test la sauvegarde avec analyse par jour"""
    test_data = {
        "jours": [
            {
                "date": "2025-06-24",
                "temperature_moyenne": 22.5,
                "temperature_min": 15.0,
                "temperature_max": 30.0
            }
        ],
        "periode": {
            "temperature_moyenne_totale": 22.5,
            "nombre_jours": 1
        }
    }
    
    filepath = tmp_path / "meteo.json"
    save_results(test_data, str(filepath))
    
    assert filepath.exists()
    
    with open(filepath, 'r') as f:
        saved_data = json.load(f)
    
    assert len(saved_data["resultats"]["jours"]) == 1
    assert saved_data["resultats"]["jours"][0]["date"] == "2025-06-24"


# Test d'intégration
def test_integration_avec_vraies_donnees(tmp_path):
    """Test avec la structure réelle de l'API"""
    real_data = {
        "hourly": {
            "time": [
                "2025-06-24T00:00", "2025-06-24T01:00", "2025-06-24T02:00",
                "2025-06-24T03:00", "2025-06-24T04:00", "2025-06-24T05:00",
                "2025-06-24T06:00", "2025-06-24T07:00", "2025-06-24T08:00",
                "2025-06-24T09:00", "2025-06-24T10:00", "2025-06-24T11:00",
                "2025-06-24T12:00", "2025-06-24T13:00", "2025-06-24T14:00",
                "2025-06-24T15:00", "2025-06-24T16:00", "2025-06-24T17:00",
                "2025-06-24T18:00", "2025-06-24T19:00", "2025-06-24T20:00",
                "2025-06-24T21:00", "2025-06-24T22:00", "2025-06-24T23:00"
            ],
            "temperature_2m": [
                16.8, 15.0, 14.6, 14.1, 13.6, 14.0, 15.4, 17.2, 19.2, 
                21.2, 23.2, 24.9, 26.5, 28.4, 29.3, 29.8, 29.9, 29.7, 
                29.3, 28.5, 27.3, 26.1, 25.1, 24.1
            ]
        }
    }
    
    analysis = analyze_weather_by_day(real_data)
    
    assert len(analysis["jours"]) == 1
    assert analysis["jours"][0]["date"] == "2025-06-24"
    assert analysis["jours"][0]["temperature_min"] == 13.6
    assert analysis["jours"][0]["temperature_max"] == 29.9


# Tests pour la visualisation
@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.show')
def test_create_temperature_graph(mock_show, mock_savefig):
    """Test la création du graphique de température"""
    test_data = {
        "jours": [
            {"date": "2025-06-24", "temperature_moyenne": 22.7},
            {"date": "2025-06-25", "temperature_moyenne": 26.4},
            {"date": "2025-06-26", "temperature_moyenne": 22.0}
        ],
        "periode": {
            "temperature_moyenne_totale": 23.7
        }
    }
    
    create_temperature_graph(test_data)
    
    mock_show.assert_called_once()
    mock_savefig.assert_called_once_with('temperatures_paris.png', dpi=300, bbox_inches='tight')


def test_graph_with_full_week_data():
    """Test avec des données d'une semaine complète"""
    test_data = {
        "jours": [
            {"date": "2025-06-24", "temperature_moyenne": 22.7, "temperature_min": 13.6, "temperature_max": 29.9},
            {"date": "2025-06-25", "temperature_moyenne": 26.4, "temperature_min": 18.3, "temperature_max": 35.7},
            {"date": "2025-06-26", "temperature_moyenne": 22.0, "temperature_min": 18.1, "temperature_max": 26.0},
            {"date": "2025-06-27", "temperature_moyenne": 24.6, "temperature_min": 19.3, "temperature_max": 29.1},
            {"date": "2025-06-28", "temperature_moyenne": 26.0, "temperature_min": 18.7, "temperature_max": 33.6},
            {"date": "2025-06-29", "temperature_moyenne": 24.2, "temperature_min": 18.7, "temperature_max": 30.0},
            {"date": "2025-06-30", "temperature_moyenne": 27.5, "temperature_min": 20.1, "temperature_max": 35.9}
        ],
        "periode": {
            "temperature_moyenne_totale": 24.8
        }
    }
    
    # Le test doit passer sans erreur
    with patch('matplotlib.pyplot.show'):
        with patch('matplotlib.pyplot.savefig'):
            create_temperature_graph(test_data)