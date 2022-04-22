from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Name = models.CharField(max_length=30)
    Address = models.CharField(max_length=200)
    age = models.IntegerField()
    Xray_image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.Name