from wtforms import IntegerField, Form, StringField
from wtforms.validators import DataRequired, Length, NumberRange

from controllers.forms.validators.form_validators import client_number_form_validator, transaction_title_form_validator

class NewTranactionForm(Form):
    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            transaction_title_form_validator
        ],
        render_kw={"placeholder": "Title"},
    )
    value = IntegerField(
        "Value",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ],
        render_kw={"placeholder": "Value"},
    )
    to = StringField(
        "To",
        validators=[
            DataRequired(),
            Length(min=5, max=5),
            client_number_form_validator,
        ],
        render_kw={"placeholder": "Recipient client number"},
    )
