class Client:
    def __init__(self, chat_id, username=None, phone=None, iin=None, firstname=None, lastname=None, second_phone=None,
                 doc_images=None, address=None):
        self.chat_id = chat_id
        self.username = username
        self.phone = phone
        self.iin = iin
        self.firstname = firstname
        self.lastname = lastname
        self.second_phone = second_phone
        self.doc_images = doc_images
        self.address = address
