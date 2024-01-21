from datetime import datetime


def get_date_from_str(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
