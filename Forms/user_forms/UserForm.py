from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators
from wtforms.fields import DateField


class UserForm(FlaskForm):
    user_name = StringField("Name: ", [
        validators.DataRequired("Please enter your name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])
    user_email = StringField("Email: ", [
        validators.DataRequired("Please enter your name."),
        validators.Email("Wrong email format")
    ])

    user_birthday = DateField("Birthday: ", [validators.DataRequired("Please enter birthday.")])

    user_phone = StringField("Phone: ", [validators.DataRequired("Please enter your phone."),
                                         validators.Length(10)])

    submit = SubmitField("Save")

    def validate_birthday(self):
        return bool(self.user_birthday.data.year > 1900)