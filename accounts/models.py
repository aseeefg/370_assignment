from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name , last_name, username, email, password=None, is_doctor=False, is_patient=False):
        if not email:
            raise ValueError('Email address is not given')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email= self.normalize_email(email),
            username = username,
            first_name= first_name,
            last_name = last_name,
            is_doctor= is_doctor,    # Added this
            is_patient= is_patient,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user 
    def create_superuser(self, first_name, last_name, email, username , password):
        user = self.create_user(
            email= self.normalize_email(email),
            username = username,
            first_name= first_name,
            last_name = last_name,
            password =password,
            # Admins are neither doctors nor patients by default
            is_doctor=False,
            is_patient=False,
        )

        user.is_admin= True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin= True
        user.is_active=True
        user.save(using= self._db)
        return user 





class Account(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    first_name= models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number= models.CharField(max_length=50)

# required
    date_joined= models.DateField(auto_now_add=True)
    last_login= models.DateField(auto_now=True)
    is_admin= models.BooleanField(default=False)
    is_staff =models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_superadmin= models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username', 'first_name', 'last_name']
    objects= MyAccountManager()
    def  __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True



