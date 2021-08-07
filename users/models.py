from django.db import models

class User(models.Model):
    username         = models.CharField(max_length = 50,unique=True)
    password         = models.CharField(max_length = 200)
    name             = models.CharField(max_length = 50)
    nickname         = models.CharField(max_length = 50, null=True)
    email            = models.CharField(max_length = 320,unique=True)
    phone_number     = models.CharField(max_length = 50,unique=True)
    address          = models.CharField(max_length = 300, null=True)
    created_at       = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "users"