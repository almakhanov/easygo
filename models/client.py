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

    def __str__(self):
        return f"Client(chat_id={self.chat_id}, username={self.username}, phone={self.phone}, iin={self.iin}, firstname={self.firstname}, lastname={self.lastname}, second_phone={self.second_phone}, doc_images={self.doc_images}, address={self.address})"
