from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, FloatField, IntegerField, SelectField
from wtforms import validators
from wtforms.fields import DateField


class AutoFormEdit(FlaskForm):
    auto_id = HiddenField("Auto ID: ")
    auto_name = StringField("Name: ", [validators.Length(2, 20, "Name should be from 3 to 20 symbols")])
    auto_mark = StringField("Auto mark: ", [validators.Length(2, 20, "Mark should be from 3 to 20 symbols")])
    fuel_consumption = FloatField("Fuel consumption: ", [validators.NumberRange(1, 1000, "Name should be from 1 to 1000 symbols")])
    emission = FloatField("Fuel consumption: ", [validators.NumberRange(1, 1000, "Name should be from 1 to 1000 symbols")])
    fuel_type = SelectField("Choose type: ", choices=[
        ('fuel_type', 'diesel'),
        ('fuel_type', 'benzin'),
        ('fuel_type', 'electric'),
        ('fuel_type', 'hybrid')
    ])

    submit = SubmitField("Save")

