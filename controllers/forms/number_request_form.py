from wtforms import Form, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput

from controllers.forms.validators.form_validators import password_form_validator


class NumberRequestForm(Form):
    password = StringField(
        "Password",
        validators=[
            DataRequired(),
            password_form_validator,
        ],
        render_kw={"placeholder": "password"},
        widget=PasswordInput(hide_value=True),
    )
