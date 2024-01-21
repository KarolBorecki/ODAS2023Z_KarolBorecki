from wtforms import EmailField, Form, StringField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.widgets import PasswordInput

from controllers.forms.validators.form_validators import (
    login_form_validator,
    password_form_validator,
)


class EditAccountForm(Form):
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
    oldPassword = StringField(
        "New password",
        validators=[
            DataRequired(),
        ],
        render_kw={"placeholder": "Old password"},
        widget=PasswordInput(hide_value=True),
    )
    newPassword1 = StringField(
        "New password",
        validators=[
            DataRequired(),
            Length(min=8),
            password_form_validator,
        ],
        render_kw={"placeholder": "New password"},
        widget=PasswordInput(hide_value=True),
    )
    newPassword2 = StringField(
        "Repeat new password",
        validators=[EqualTo("newPassword1", message="Passwords must match")],
        render_kw={"placeholder": "Repeat new password"},
        widget=PasswordInput(hide_value=True),
    )
