from django.db import models

from users.models    import User
from products.models import Product, Option

# Create your models here.
class Cart(models.Model):
    user     = models.ForeignKey('users.User', on_delete = models.CASCADE)
    product  = models.ForeignKey('products.Product', on_delete = models.CASCADE)
    option   = models.ForeignKey('products.Option', on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'carts'