from wtforms import EmailField, Form
from wtforms.validators import DataRequired, Email


class PasswordRestoreRequestForm(Form):
    email = EmailField(
        "Email address",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email address"},
    )
