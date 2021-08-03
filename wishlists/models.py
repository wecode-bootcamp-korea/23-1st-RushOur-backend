from django.db import models

from users.models    import User
from products.models import Product

# Create your models here.
class Wishlist(models.Model):
    user    = models.ForeignKey('users.User', on_delete = models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete = models.CASCADE)

    class Meta:
        db_table = 'wishlists'