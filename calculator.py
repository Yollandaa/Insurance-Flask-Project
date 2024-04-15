# For Vihicle quote
from datetime import datetime


def car_quote(age, license_year_issue, car_type, year, accidents=0):
    car_type_costs = [
        ("Sedan", 0),
        ("Hatchback", 2),
        ("Coupe", 4),
        ("Wagon", 6),
        ("SUV (Sport Utility Vehicle)", 8),
        ("Crossover", 10),
        ("Electric Vehicle (EV)", 12),
        ("Hybrid", 13),
        ("Convertible", 14),
        ("Luxury", 15),
    ]
    premium_cost = 4.5  # Base rate for the quote
    age_factor = 0.02  # Increase rate per year of age
    history_factor = 0.05  # Increase rate per accident or traffic violation

    # Adjust premium amount based on car type
    filtered_car = next((cost for car, cost in car_type_costs if car == car_type), None)
    premium_cost += filtered_car

    # Adjust premium amount based on age and license years
    years_since_issue = 2024 - license_year_issue
    premium_cost += premium_cost * (age * age_factor)
    premium_cost += premium_cost * (years_since_issue * age_factor)

    # Adjust based on accidents or driving history
    premium_cost += premium_cost * (accidents * history_factor)

    # Adjust premium amount based on the year of the car
    current_year = datetime.now().year
    car_age = current_year - year
    if car_age > 10:
        # Example: Increase premium by 2% for each year beyond 10 years old
        premium_cost += premium_cost * (car_age - 10) * 0.02

    return premium_cost


def get_coverage(premium_amount):
    if premium_amount < 200:
        return 15000
    elif 200 <= premium_amount < 300:
        return 25000
    else:
        return 50000


if __name__ == "__main__":
    print(car_quote(18, 2024, "SUV (Sport Utility Vehicle)"))
