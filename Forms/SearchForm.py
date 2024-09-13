from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms import validators


class SearchForm(FlaskForm):
    type_field = SelectField('Choose field', choices=[
        ('user_email', 'user_email'),
        ('user_name', 'user_name'),
        ('user_phone', 'user_phone'),
        ('auto_name', 'auto_name'),
        ('fuel_consumption', 'fuel_consumption'),
        ('emission', 'emission'),
        ('fuel_type', 'fuel_type'),
    ])
    search_value = StringField("Value: ", [validators.DataRequired('should not be empty value')])

    submit = SubmitField("Search")
