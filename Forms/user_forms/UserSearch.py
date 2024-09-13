from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms import validators


class UserSearch(FlaskForm):
    search_value = StringField("Бренд транспорту: ", [validators.DataRequired('Це поле не може бути порожнім.'), validators.Length(3, 30, "Довжина цього поля має сягати від 3 до 30 символів")])
    submit = SubmitField("Пошук")
