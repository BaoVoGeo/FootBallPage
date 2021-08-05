from django.db import models

class AuthUser (models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    img_avt_id = models.ImageField()
    
    def __str__(self):
        return self.username
    
    
# Create your models here.
