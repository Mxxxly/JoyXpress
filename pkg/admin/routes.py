from flask import render_template,flash,redirect,url_for,request
from pkg.admin import adminobj
from pkg.models import db, State, City, ShippingRate


NIGERIA_LOCATIONS = {
    "Abia": ["Aba", "Umuahia", "Ohafia", "Arochukwu"],
    "Adamawa": ["Yola", "Mubi", "Numan", "Ganye"],
    "Akwa Ibom": ["Uyo", "Ikot Ekpene", "Eket", "Oron"],
    "Anambra": ["Awka", "Onitsha", "Nnewi", "Ekwulobia"],
    "Bauchi": ["Bauchi", "Azare", "Misau", "Jama’are"],
    "Bayelsa": ["Yenagoa", "Ogbia", "Brass", "Nembe"],
    "Benue": ["Makurdi", "Gboko", "Otukpo", "Katsina-Ala"],
    "Borno": ["Maiduguri", "Biu", "Dikwa", "Gwoza"],
    "Cross River": ["Calabar", "Ikom", "Ogoja", "Obudu"],
    "Delta": ["Asaba", "Warri", "Sapele", "Ughelli"],
    "Ebonyi": ["Abakaliki", "Afikpo", "Onueke"],
    "Edo": ["Benin City", "Auchi", "Ekpoma"],
    "Ekiti": ["Ado-Ekiti", "Ikere", "Omuo"],
    "Enugu": ["Enugu", "Nsukka", "Awgu", "Udi"],
    "Gombe": ["Gombe", "Kaltungo", "Dukku"],
    "Imo": ["Owerri", "Orlu", "Okigwe"],
    "Jigawa": ["Dutse", "Hadejia", "Gumel"],
    "Kaduna": ["Kaduna", "Zaria", "Kafanchan"],
    "Kano": ["Kano", "Wudil", "Rano", "Gaya"],
    "Katsina": ["Katsina", "Daura", "Funtua"],
    "Kebbi": ["Birnin Kebbi", "Argungu", "Yauri"],
    "Kogi": ["Lokoja", "Okene", "Idah"],
    "Kwara": ["Ilorin", "Offa", "Omu-Aran"],
    "Lagos": ["Ikeja", "Lekki", "Yaba", "Surulere", "Ikorodu", "Badagry"],
    "Nasarawa": ["Lafia", "Keffi", "Akwanga"],
    "Niger": ["Minna", "Bida", "Suleja"],
    "Ogun": ["Abeokuta", "Ijebu-Ode", "Ota", "Sagamu"],
    "Ondo": ["Akure", "Owo", "Ondo", "Ikare"],
    "Osun": ["Osogbo", "Ile-Ife", "Ilesa"],
    "Oyo": ["Ibadan", "Ogbomosho", "Oyo", "Iseyin"],
    "Plateau": ["Jos", "Bukuru", "Pankshin"],
    "Rivers": ["Port Harcourt", "Obio-Akpor", "Bonny", "Ahoada"],
    "Sokoto": ["Sokoto", "Wamako", "Tambuwal"],
    "Taraba": ["Jalingo", "Wukari", "Takum"],
    "Yobe": ["Damaturu", "Potiskum", "Gashua"],
    "Zamfara": ["Gusau", "Kaura Namoda", "Talata Mafara"],
    "FCT": ["Abuja", "Garki", "Wuse", "Maitama", "Kubwa"]
}





@adminobj.route('/')
def home():
    return render_template('admin/index.html')


@adminobj.route('/dashboard/')
def dashboard():
    return render_template('admin/dashboard.html')


@adminobj.route('/create/states-cities')
def create_states_cities():
    """
    Admin route to seed Nigerian states and their cities
    """
    for state_name, cities in NIGERIA_LOCATIONS.items():
        # Check if state already exists
        state = State.query.filter_by(name=state_name).first()
        if not state:
            state = State(name=state_name)
            db.session.add(state)
            db.session.flush()  # make state.id available

        # Add cities
        for city_name in cities:
            exists = City.query.filter_by(name=city_name, state_id=state.id).first()
            if not exists:
                db.session.add(City(name=city_name, state_id=state.id))

    db.session.commit()
    return "Nigerian states and cities created successfully!"


@adminobj.route('/admin/setup_rates', methods=['GET', 'POST'])
def setup_rates():
    """Route to initialize or update all required shipping rates."""
    
    # 1. Define all vehicle types and their initial/default values
    # You can adjust these prices as needed.
    rate_defaults = {
        'bike': {'base_price': 1500.00, 'price_per_kg': 50.00, 'distance_multiplier': 1.00},
        'van': {'base_price': 3500.00, 'price_per_kg': 150.00, 'distance_multiplier': 2.50},
        'bus': {'base_price': 6000.00, 'price_per_kg': 250.00, 'distance_multiplier': 4.00},
    }
    
    updated_count = 0
    
    try:
        for rate_type, defaults in rate_defaults.items():
            # Check if rate already exists
            rate = ShippingRate.query.filter_by(rate_type=rate_type).first()
            
            if rate is None:
                # Insert new rate
                rate = ShippingRate(
                    rate_type=rate_type,
                    base_price=defaults['base_price'],
                    price_per_kg=defaults['price_per_kg'],
                    distance_multiplier=defaults['distance_multiplier']
                )
                db.session.add(rate)
                updated_count += 1
            else:
                # If you ever use a POST method here, you would update existing rates:
                # rate.base_price = defaults['base_price'] 
                # ...
                pass # Skipping updates for simplicity on a GET request
                
        db.session.commit()
        
        if updated_count > 0:
            flash(f"SUCCESS: Initial rates for {updated_count} vehicle types inserted. You can now calculate rates.", 'success')
        else:
            flash("Rates already configured. No changes made.", 'info')

    except Exception as e:
        db.session.rollback()
        flash(f"FATAL ERROR setting up rates: {str(e)}", 'danger')

    # Redirect to a safe page after setup
    return redirect(url_for('bpshipment.new_shipment'))
