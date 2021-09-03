from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    label_color = models.CharField(max_length=25, blank=True, null=True)
    label = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField()
    img = models.CharField(max_length=500)
    

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ForeignKey(Item, on_delete=CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.items.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.items.price

    def get_total_discount_price(self):
        return self.quantity * self.items.discount_price
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_price()
    
    def get_final_price(self):
        if self.items.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total