from django.db import models

from products.models import Product
# Create your models here.

class Banner(models.Model):
    image_url = models.CharField(max_length=500)
    product   = models.ForeignKey('products.Product', on_delete = models.CASCADE)

    class Meta:
        db_table = 'banners'