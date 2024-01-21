from wtforms import EmailField, Form, StringField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from wtforms.widgets import PasswordInput

from controllers.forms.validators.form_validators import (
    document_number_form_validator,
    login_form_validator,
    password_form_validator,
)


class RegistrationForm(Form):
    username = StringField(
        "Username",
        validators=[DataRequired(), login_form_validator],
        render_kw={"placeholder": "Username"},
    )
    email = EmailField(
        "Email address",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email address"},
    )
    password1 = StringField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
            password_form_validator,
        ],
        render_kw={"placeholder": "Password"},
        widget=PasswordInput(hide_value=True),
    )
    password2 = StringField(
        "Repeat Password",
        validators=[EqualTo("password1", message="Passwords must match")],
        render_kw={"placeholder": "Repeat password"},
        widget=PasswordInput(hide_value=True),
    )
    documentNumber = StringField(
        "Document Number",
        validators=[
            DataRequired(),
            Length(min=8, max=8),
            document_number_form_validator,
        ],
        render_kw={"placeholder": "Document number"},
    )
