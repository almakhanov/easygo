class Rent:
    def __init__(self, chat_id, client_fullname, product_number, product_type, start_date, end_date, price, payment_type, rent_status):
        self.chat_id = chat_id
        self.client_fullname = client_fullname
        self.product_number = product_number
        self.product_type = product_type
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.payment_type = payment_type
        self.rent_status = rent_status
