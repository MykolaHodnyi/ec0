from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms import validators
from wtforms.fields import DateField


class UserEdit(FlaskForm):
    user_name = StringField("Name: ", [validators.Length(3, 20, "Name should be from 3 to 20 symbols")])
    user_email = HiddenField("Email: ", [validators.Email("Wrong email format")])
    user_birthday = DateField("Birthday: ", [validators.DataRequired("Please enter birthday.")])
    user_phone = StringField("Phone: ", [validators.Length(10)])

    submit = SubmitField("Save")

    def validate_birthday(self):
        return bool(self.user_birthday.data.year > 1900)
