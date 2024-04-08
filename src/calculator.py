# For Vihicle quote
def car_quote(age, license_year_issue, car_type, accidents=0):
    car_type_costs = [
        ("Sedan", 0),
        ("Hatchback", 5),
        ("Coupe", 10),
        ("Wagon", 15),
        ("SUV (Sport Utility Vehicle)", 20),
        ("Crossover", 25),
        ("Electric Vehicle (EV)", 30),
        ("Hybrid", 35),
        ("Convertible", 40),
        ("Luxury", 80),
    ]
    premium_cost = 100  # Base rate for the quote
    age_factor = 0.02  # Increase rate per year of age
    history_factor = 0.05  # Increase rate per accident or traffic violation

    # Do not cover people not within 18-65
    if age < 18 or age > 65:
        raise ValueError("Age must be between 18 and 65")

    # Adjust premium amount based on car type
    filtered_car = next((cost for car, cost in car_type_costs if car == car_type), None)
    premium_cost += filtered_car

    # Adjust premium amount based on age and license years
    years_since_issue = 2024 - license_year_issue
    premium_cost += premium_cost * (age * age_factor)
    premium_cost += premium_cost * (years_since_issue * age_factor)

    # Adjust based on accidents or driving history
    premium_cost += premium_cost * (accidents * history_factor)

    return premium_cost


# Might not be necessary to do other calculations, can just ask for details then consultant will contact them


def determine_coverage(premium_amount):
    if premium_amount < 200:
        return "R15,000 coverage"
    elif 200 <= premium_amount < 300:
        return "R25,000 coverage"
    else:
        return "Custom coverage based on premium amount"


if __name__ == "__main__":
    print(car_quote(18, 2024, "SUV (Sport Utility Vehicle)"))
