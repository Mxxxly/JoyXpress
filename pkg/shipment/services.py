# pkg/shipment/services.py (Final Server-Side Calculation Logic)

from pkg.models import City, State, ShippingRate 
import random

def generate_tracking_number():
    """Generates a unique 10-digit tracking number."""
    return 'JX' + ''.join(str(random.randint(0, 9)) for _ in range(8))


def calculate_rate(pickup_city_id, delivery_city_id, weight_kg, delivery_type):
    """Calculates the shipment rate based on database rates and a fixed distance."""
    
    # 1. Look up Rate Tier
    rate_tier = ShippingRate.query.filter_by(rate_type=delivery_type).first()
    
    if not rate_tier:
        # This will raise an exception caught by the route, which displays an error flash
        raise ValueError(f"Rate tier '{delivery_type}' is not configured in the database. (Check Admin setup.)")

    # 2. Determine Distance Factor 
    
    # Get City objects
    pickup_city = City.query.get(pickup_city_id)
    delivery_city = City.query.get(delivery_city_id)
    
    # CRITICAL FIX: Safety Check for City Existence 
    if not pickup_city:
        raise ValueError(f"Pickup city ID is invalid. Please select a City.")
    if not delivery_city:
        raise ValueError(f"Delivery city ID is invalid. Please select a City.")
    
    
    # Logic: Intra-state vs. Inter-state
    if pickup_city.state_id == delivery_city.state_id:
        distance_km = 50.0  # Intra-state assumption
    else:
        distance_km = 450.0 # Inter-state assumption

    # 3. Calculation Logic
    
    base_charge = rate_tier.base_price
    
    # Distance charge: Assumed Distance * Price Per Assumed KM
    distance_charge = distance_km * rate_tier.distance_multiplier
    
    # Weight charge: Weight * Price Per KG
    weight_charge = weight_kg * rate_tier.price_per_kg

    # Final Amount (Rounded to two decimal places)
    calculated_amount = round(base_charge + distance_charge + weight_charge, 2)

    # 4. Return the result
    return {
        'distance_km': distance_km,
        'calculated_amount': calculated_amount
    }