from first_exo import est_pair
from first_exo import convert_minutes
from first_exo import convert_list_minutes

def test_est_pair():
    """Test the est_pair function."""
    assert est_pair(2) == True, "2 should be even"
    assert est_pair(3) == False, "3 should not be even"
    assert est_pair(0) == True, "0 should be even"
    assert est_pair(-2) == True, "-2 should be even"
    assert est_pair(-3) == False, "-3 should not be even"
    
    
    
def test_convert_minutes():
    """Test the convert_minutes function."""
    assert convert_minutes(60) == "1 heure(s) et 0 minute(s)", "60 minutes should be 1 hour and 0 minutes"
    assert convert_minutes(120) == "2 heure(s) et 0 minute(s)", "120 minutes should be 2 hours and 0 minutes"
    assert convert_minutes(90) == "1 heure(s) et 30 minute(s)", "90 minutes should be 1 hour and 30 minutes"
    assert convert_minutes(0) == "0 heure(s) et 0 minute(s)", "0 minutes should be 0 hours and 0 minutes"
    assert convert_minutes(-30) == "-1 heure(s) et 30 minute(s)", "-30 minutes should be -1 hour and 30 minutes"
    

def test_convert_list_minutes():
    """Test the convert_list_minutes function with a list of minutes."""
    minutes_list = [60, 120, 90, 0, -30]
    expected_results = [
        "1 heure(s) et 0 minute(s)",
        "2 heure(s) et 0 minute(s)",
        "1 heure(s) et 30 minute(s)",
        "0 heure(s) et 0 minute(s)",
        "-1 heure(s) et 30 minute(s)"
    ]
    
    assert convert_list_minutes(minutes_list) == expected_results, "convert_list_minutes did not return expected results"
