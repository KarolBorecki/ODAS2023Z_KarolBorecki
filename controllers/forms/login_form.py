from wtforms import Form, IntegerField, StringField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput

from controllers.forms.validators.form_validators import (
    login_form_validator,
    password_form_validator,
)


class LoginForm(Form):
    username = StringField(
        "Username",
        validators=[DataRequired(), login_form_validator],
        render_kw={"placeholder": "username"},
    )
    password = StringField(
        "Password",
        validators=[
            DataRequired(),
            password_form_validator,
        ],
        render_kw={"placeholder": "password"},
        widget=PasswordInput(hide_value=True),
    )
    digit_0 = StringField(
        "Digit 0",
        validators=[DataRequired(), Length(min=1, max=1)],
    )
    digit_1 = StringField(
        "Digit 1",
        validators=[DataRequired(), Length(min=1, max=1)],
    )
    digit_2 = StringField(
        "Digit 2",
        validators=[DataRequired(), Length(min=1, max=1)],
    )
    digit_3 = StringField(
        "Digit 3",
        validators=[DataRequired(), Length(min=1, max=1)],
    )
    digit_4 = StringField(
        "Digit 4",
        validators=[DataRequired(), Length(min=1, max=1)],
    )
    digit_5 = StringField(
        "Digit 5",
        validators=[DataRequired(), Length(min=1, max=1)],
    )
    digit_6 = StringField(
        "Digit 6",
        validators=[DataRequired(), Length(min=1, max=1)],
    )
    digit_7 = StringField(
        "Digit 7",
        validators=[DataRequired(), Length(min=1, max=1)],
    )