class Product:
    def __init__(self, number, vin, images, model, status, product_type):
        self.number = number
        self.vin = vin
        self.images = images
        self.model = model
        self.status = status
        self.product_type = product_type

    def to_dict(self):
        return {
            'number': self.number,
            'vin': self.vin,
            'images': self.images,
            'model': self.model,
            'status': self.status,
            'product_type': self.product_type
        }

    def __str__(self):
        return f"Номер мопеда: {self.number}\n" \
               f"VIN номер {self.vin}\n" \
               f"Модель: {self.model}"
