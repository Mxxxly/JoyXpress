# pkg/shipment/form.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, SubmitField,IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional,ValidationError
from pkg.models import State, City # Ensure this import path is correct


class DynamicSelectField(SelectField):
    """A SelectField that allows dynamic choices added by JavaScript."""
    def pre_validate(self, form):
        # Override the default SelectField pre_validate method
        # which checks the submitted value against the choices list.
        # By doing nothing, we skip that strict check.
        pass


class NewShipmentForm(FlaskForm):
    # Receiver Details (remain the same)
    receiver_name = StringField("Receiver Full Name", validators=[DataRequired(), Length(max=120)])
    receiver_phone = StringField("Receiver Phone", validators=[DataRequired(), Length(max=20)])

    # Pickup Details - State remains SelectField, City changes to IntegerField
    pickup_address = TextAreaField("Pickup Address", validators=[DataRequired(), Length(max=255)])
    pickup_state = SelectField("Pickup State", coerce=int, validators=[DataRequired()])
    # CRITICAL CHANGE: Use IntegerField to allow any value, then validate manually
    pickup_city = DynamicSelectField("Pickup City", coerce=int, validators=[DataRequired(message="Please select a Pickup City.")])
    
    # Delivery Details
    delivery_address = TextAreaField("Delivery Address", validators=[DataRequired(), Length(max=255)])
    delivery_state = SelectField("Delivery State", coerce=int, validators=[DataRequired()])
    # CRITICAL CHANGE: Use IntegerField to allow any value, then validate manually
    delivery_city = DynamicSelectField("Delivery City", coerce=int, validators=[DataRequired(message="Please select a Delivery City.")])

    # Package Details (remain the same)
    package_weight = FloatField("Package Weight (kg)", validators=[DataRequired(), NumberRange(min=0.1, message="Weight must be positive.")])
    delivery_type = SelectField("Delivery Type", choices=[
        ('bike', 'Motorcycle/Bike (Quick & Small)'),
        ('van', 'Van/Bus (Standard & Medium)'),
        ('truck', 'Truck (Large/Heavy)')
    ], validators=[DataRequired()])
    
    # Hidden fields for calculated data (remain the same)
    distance_km = FloatField("Distance (km)", validators=[Optional()])
    calculated_amount = FloatField("Calculated Amount", validators=[Optional()])

    submit = SubmitField("Confirm Shipment & Proceed to Payment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate state choices globally
        state_choices = [(s.id, s.name) for s in State.query.order_by(State.name).all()]
        self.pickup_state.choices = [(0, 'Select State')] + state_choices
        self.delivery_state.choices = [(0, 'Select State')] + state_choices
        
    # --- Custom Validation for City IDs ---
    def validate_pickup_city(self, field):
        if field.data and not City.query.get(field.data):
            raise ValidationError("Invalid Pickup City selected. Please select from the list.")

    def validate_delivery_city(self, field):
        if field.data and not City.query.get(field.data):
            raise ValidationError("Invalid Delivery City selected. Please select from the list.")