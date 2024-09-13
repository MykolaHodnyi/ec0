from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, FloatField, SelectField
from wtforms import validators


class AutoForm(FlaskForm):
    auto_id = IntegerField("ID: ", [
        validators.DataRequired("Please enter your place price."),
        validators.NumberRange(1, 1000, "Name should be from 1 to 1000 symbols")
    ])

    auto_name = StringField("Auto name: ", [
        validators.DataRequired("Please enter auto name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    auto_mark = StringField("Auto mark: ", [
        validators.DataRequired("Please enter auto mark."),
        validators.Length(3, 20, "Mark should be from 3 to 20 symbols")
    ])

    fuel_consumption = FloatField("Fuel consumption: ", [
        validators.DataRequired("Please enter fuel consumption."),
        validators.NumberRange(0, 1000, "Mark should be from 3 to 1000 symbols")
    ])

    emission = FloatField("Emission: ", [
        validators.DataRequired("Please enter emission."),
        validators.NumberRange(0, 1000, "Emission should be from 3 to 1000 symbols")
    ])

    fuel_type = SelectField("Choose type: ", choices=[
        ('fuel_type', 'diesel'),
        ('fuel_type', 'benzin'),
        ('fuel_type', 'electric'),
        ('fuel_type', 'hybrid')
    ])

    submit = SubmitField("Save")