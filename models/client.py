class Client:
    def __init__(self, chat_id, username, phone=None, iin=None, firstname=None, surname=None, second_phone=None,
                 doc_images=None, age=None, address=None):
        self.chat_id = chat_id
        self.username = username
        self.phone = phone
        self.iin = iin
        self.firstname = firstname
        self.surname = surname
        self.second_phone = second_phone
        self.doc_images = doc_images
        self.age = age
        self.address = address
