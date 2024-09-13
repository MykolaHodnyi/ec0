from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
from wtforms.fields import DateField


class Registration(FlaskForm):
    user_email = StringField("Email: ", [
        validators.DataRequired("Будь ласка, введіть свою електронну адресу."),
        validators.Email("Неправильний формат електронної пошти")
    ])
    user_first_name = StringField("Ім'я: ", [
        validators.DataRequired("Будь ласка, введіть своє ім'я."),
        validators.Length(2, 30, "Ім'я має бути від 2 до 30 символів")
    ])
    user_second_name = StringField("Прізвище:", [
        validators.DataRequired("Будь ласка, введіть своє ім'я."),
        validators.Length(2, 30, "Прізвище має бути від 2 до 30 символів")
    ])
    user_phone = StringField("Телефон:", [validators.DataRequired("Будь ласка, введіть свій телефон."), validators.Length(min=10)])
    user_birthday = DateField("День народження:", [validators.DataRequired("Будь ласка, введіть день народження.")])
    user_password = PasswordField("Пароль:", [
        validators.DataRequired("Будь ласка, введіть свій пароль."),
        validators.Length(min=8)
    ])
    user_confirm_password = PasswordField("Підтвердіть пароль:", [
        validators.DataRequired("Будь ласка, введіть свій пароль."),
        validators.Length(min=8),
        validators.EqualTo('user_password', message='Паролі мають збігатися!')
    ])
    submit = SubmitField("Зареєструватися")
    def validate_birthday(self):
        return bool(self.user_birthday.data.year > 1900)
