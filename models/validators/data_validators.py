import re

REGEX_NUMBER_AND_LETTERS = "[a-zA-Z0-9]+"


def validate_document_number(document_number):
    return re.fullmatch("[0-9]{8}", document_number)


def validate_client_number(client_number):
    return re.fullmatch("[0-9]{5}", client_number)


def validate_login(login):
    return re.fullmatch("[a-zA-Z0-9]+", login)


def validate_password(password):
    return re.fullmatch(
        "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@_$%^&*-]).{8,}$", password
    )


def validate_transaction_title(title):
    return re.fullmatch("[a-zA-Z0-9]+", title)


def validate_transaction_value(value):
    return re.fullmatch("[0-9]+", value)
