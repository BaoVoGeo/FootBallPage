from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

    
class MyAccountManager(BaseUserManager): 
    def create_user(self,  first_name, last_name, email, password=None): 
        # if not email: 
        #     raise ValueError('Email address is required') 
        # Tạo đối tượng user mới 
        
        user = self.model( first_name=first_name, last_name=last_name, 
                          email=self.normalize_email(email=email), # Chuyển email về dạng bình thường   
                          ) 
        user.set_password(password)
        user.save(using=self._db) 
        return user 
    
    def create_superuser(self,first_name, last_name,  email, password): 
        user = self.create_user( first_name=first_name, last_name=last_name, email=self.normalize_email(email=email), password=password,  ) 
        user.is_admin = True 
        user.is_active = True 
        user.is_staff = True 
        user.is_superadmin = True 
        user.save(using=self._db) 
        return user

profile_default = 'images/avatar/messi.jpg'
class Account(AbstractBaseUser): 
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    email = models.EmailField(max_length=100, unique=True) 
    phone_number = models.CharField(max_length=50) # required 
    date_joined = models.DateTimeField(auto_now_add=True) 
    last_login = models.DateTimeField(auto_now_add=True) 
    is_admin = models.BooleanField(default=False) 
    is_staff = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=False) 
    is_superadmin = models.BooleanField(default=False) 
    profile_avt = models.ImageField(upload_to='images/avatar', null=True, blank=True, default="media/images/avatar.png")
    
    USERNAME_FIELD = 'email' # Trường quyết định khi login 
    REQUIRED_FIELDS = [  'first_name', 'last_name'] 
    # Các trường yêu cầu khi đk tài khoản (mặc định đã có email), mặc định có password 
    objects = MyAccountManager() 
    
    def __str__(self): 
        return self.email 
    def has_perm(self, perm, obj=None): 
        return self.is_admin 
    # # Admin có tất cả quyền trong hệ thống 
    def has_module_perms(self, add_label): 
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    @property
    def get_profile_avt_url(self):
        if self.profile_avt:
            return self.profile_avt.url
        else:   
            return "media/images/avatar.png"
    
    
def get_profile_image_filepath (self,filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image(self):
    return "media/images/logo.png"