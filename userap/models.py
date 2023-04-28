from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20, default='')
    def __str__(self):
        return self.full_name

class Address(models.Model):
    user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=255, default='')
    mobile = models.CharField(max_length=20, default='')
    house_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6)

    def __str__(self):
      return f"{self.house_name} ({self.id})"