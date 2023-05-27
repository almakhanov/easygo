class Banner:
    def __init__(self, pricePerWeek, pricePerDay, model, image, product_type, left_count=0, total_count=0):
        self.pricePerWeek = pricePerWeek
        self.pricePerDay = pricePerDay
        self.model = model
        self.image = image
        self.product_type = product_type
        self.left_count = left_count
        self.total_count = total_count

    def __str__(self):
        return f"Модель: {self.model}\n" \
               f"Цена за неделю: {'{:0,.2f}'.format(self.pricePerWeek)} ₸\n" \
               f"Цена за день: {'{:0,.2f}'.format(self.pricePerDay)} ₸\n" \
               f"В наличии: {self.left_count}/{self.total_count}"

