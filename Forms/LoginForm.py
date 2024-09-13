from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class LoginForm(FlaskForm):
    user_password = PasswordField("Пароль: ", [
        validators.DataRequired("Будь ласка, введіть свій пароль")
    ])
    user_email = StringField("Email: ", [
        validators.DataRequired("Будь ласка, введіть свою електронну пошту"),
        validators.Email("Неправильний формат електронної пошти")
    ])
    submit = SubmitField("Увійти")
