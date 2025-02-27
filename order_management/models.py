from django.db import models
from bread_management.models import Bread
from user_management.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.user.username} for {self.bread.name}"