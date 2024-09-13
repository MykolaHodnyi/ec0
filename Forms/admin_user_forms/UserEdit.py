from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms import validators
from wtforms.fields import DateField


class UserEdit(FlaskForm):
    user_first_name = StringField("Ім'я: ", [validators.Length(1, 30, "Ім'я має бути від 1 до 30 символів")])
    user_second_name = StringField("Фамілія: ", [validators.Length(1, 30, "Фамілія має бути від 1 до 30 символів")])
    user_email = HiddenField("Email: ", [validators.Email("Неправильний формат електронної пошти")])
    user_birthday = DateField("День народження: ", [validators.DataRequired("Будь ласка, введіть день народження.")])
    user_phone = StringField("Телефон: ", [validators.Length(13)])
    submit = SubmitField("Зберегти")
    def validate_birthday(self):
        return bool(self.user_birthday.data.year > 1900)
