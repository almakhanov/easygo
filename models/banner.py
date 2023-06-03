class Banner:
    def __init__(
            self,
            model,
            image,
            product_type,
            left_count=0,
            total_count=0,
            price_per_week=0,
            price_per_day=0
    ):
        self.model = model
        self.image = image
        self.product_type = product_type
        self.left_count = left_count
        self.total_count = total_count
        self.price_per_week = price_per_week
        self.price_per_day = price_per_day

    def __str__(self):
        return f"Модель: {self.model}\n" \
               f"Цена за неделю: {'{:0,.2f}'.format(self.price_per_week)} ₸\n" \
               f"Цена за день: {'{:0,.2f}'.format(self.price_per_day)} ₸\n" \
               f"В наличии: {self.left_count}/{self.total_count}"

