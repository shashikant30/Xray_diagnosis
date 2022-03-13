from django.db import models

# Create your models here.
class User(models.Model):
    Name = models.CharField(max_length=30)
    Address = models.CharField(max_length=200)
    age = models.IntegerField()
    Xray_image = models.ImageField(upload_to='images/')