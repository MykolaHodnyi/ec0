from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, FloatField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms import validators, DateField


class NewUserVehicle(FlaskForm):
    vehicle_brand = StringField("Марка транспорту: ", [
        validators.DataRequired("Будь ласка, введіть марку транспорту."),
        validators.Length(3, 20, "Марка має бути від 3 до 30 символів")
    ])
    vehicle_model = StringField("Модель транспортного засобу: ", [
        validators.DataRequired("Будь ласка, введіть модель транспорту."),
        validators.Length(3, 20, "Модель має бути від 3 до 30 символів")
    ])
    fuel_consumption = FloatField("Витрата палива (л/100км):", [
        validators.NumberRange(0, 500, "Витрата палива повинна бути від 0 до 500")
    ])
    kilowatt_hour = FloatField("Кіловат-години: ")
    fuel_type = SelectField("Виберіть тип:", choices=[
        ('Diesel', 'Diesel'),
        ('Benzin', 'Benzin'),
        ('Hybrid', 'Hybrid'),
        ('Electric', 'Electric'),
        ('Human-Powered', 'Human-Powered'),
    ], default='Diesel')
    vehicle_title_image = FileField("Зображення транспорту: ",validators=[FileAllowed(['jpg', 'png', 'svg', 'jpeg'], 'Лише зображення!')])
    vehicle_year = DateField("Рік виготовлення:", [validators.DataRequired("Будь ласка, введіть рік виготовлення транспорту.")])
    vehicle_price = FloatField("Ціна(грн):", [
        validators.DataRequired("Будь ласка, введіть ціну."),
        validators.NumberRange(0, 10000000000, "Ціна повинна бути від 0 до 10000000000 символів")
    ])
    submit = SubmitField("Зберегти")
