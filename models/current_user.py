class CurrentUser:
    username = "Unknown"
    user_id = None
    document_number = 0
    is_document_number_visible = False
    client_nr = 0
    email = ""

    def __init__(self, user_id, username, document_number=0, client_nr=0, email=""):
        self.username = username
        self.user_id = user_id
        self.document_number = document_number
        self.is_document_number_visible = False
        self.client_nr = client_nr
        self.email = email
