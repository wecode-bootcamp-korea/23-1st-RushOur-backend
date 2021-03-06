from django.db import models

# Create your models here.
class Category(models.Model):
    name        = models.CharField(max_length=45)
    description = models.CharField(max_length=200)
    image_url   = models.CharField(max_length=2000)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name        = models.CharField(max_length=45)
    description = models.CharField(max_length=200)
    image_url   = models.CharField(max_length=2000)
    category    = models.ForeignKey('Category', on_delete = models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class Product(models.Model):
    name                = models.CharField(max_length=45)
    thumbnail_image_url = models.CharField(max_length=2000)
    sub_category        = models.ForeignKey('SubCategory', on_delete = models.PROTECT)
    tags                = models.ManyToManyField('Tag', related_name = 'products')

    class Meta:
        db_table = 'products'

class Option(models.Model):
    size    = models.PositiveIntegerField()
    price   = models.DecimalField(max_digits = 12, decimal_places = 2)
    product = models.ForeignKey('Product', on_delete = models.CASCADE)

    class Meta:
        db_table = 'options'

class ProductDetailImage(models.Model):
    product   = models.ForeignKey('Product', on_delete = models.CASCADE)
    image_url = models.CharField(max_length=2000)

    class Meta:
        db_table = 'product_detail_images'

class Tag(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'tags'
