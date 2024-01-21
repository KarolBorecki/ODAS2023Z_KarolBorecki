from wtforms import ValidationError
from app_settings import AppSettings

from models.validators.data_validators import validate_document_number, validate_client_number, validate_login, validate_password, validate_transaction_title, validate_transaction_value

def document_number_form_validator(form, field):
    if not validate_document_number(field.data):
        raise ValidationError('Document number needs to have 8 digits')

def client_number_form_validator(form, field):
    if not validate_client_number(field.data):
        raise ValidationError('Client number needs to have 5 digits')

def login_form_validator(form, field):
    if not validate_login(field.data):
        raise ValidationError('Login can contain only letters and numbers')

def password_form_validator(form, field):
    if not validate_password(field.data):
        raise ValidationError('Passwords needs to have at least 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 special character')
    
def transaction_title_form_validator(form, field):
    if not validate_transaction_title(field.data):
        raise ValidationError('Transaction title needs to have at least 1 character and no blank or special characters')