def main():
    """Main function to demonstrate the functionality."""
    print("Testing est_pair function:")
    print(est_pair(2))  # True
    print(est_pair(3))  # False
    print(est_pair(0))  # True
    print(est_pair(-2))  # True
    print(est_pair(-3))  # False

    print("\nTesting convert_minutes function:")
    print(convert_minutes(60))  # 1.0
    print(convert_minutes(120))  # 2.0
    print(convert_minutes(90))  # 1.5
    print(convert_minutes(0))  # 0.0
    print(convert_minutes(-30))  # -0.5

def est_pair(n):
    """Check if a number is even."""
    return n % 2 == 0


def convert_minutes(minutes):
    """Convertit un nombre entier de minutes en une chaîne indiquant heures et minutes."""
    heures = minutes // 60
    mins = abs(minutes) % 60 if minutes < 0 else minutes % 60
    signe = "-" if minutes < 0 else ""
    return f"{signe}{abs(heures)} heure(s) et {mins} minute(s)"
    
    
def convert_list_minutes(minutes_list):
    """Convertit une liste de minutes en une liste de chaînes indiquant heures et minutes."""
    return [convert_minutes(minutes) for minutes in minutes_list]


if __name__ == "__main__":
    main()