from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    birthday = models.DateField(null=False, blank=False)

# Create your models here.



        
         