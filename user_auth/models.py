from django.db import models
from django.contrib.auth.models import (
    BaseUserManager , AbstractBaseUser , AbstractUser
)

class UserManger(BaseUserManager):
    def create_user(self, email, phone, password=None):
        if not email:
            raise ValueError("User must have an email")
        user = self.model(phone=phone, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, phone, password=None):
        user = self.create_user(email=email, phone=phone, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None):
        user = self.create_user(email=email, phone=phone, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        # user.roles = 'SUPERADMIN'
        user.save(using=self._db)
        return user

class User(AbstractUser):
    user_id = models.CharField( max_length=40, unique=True )
    email = models.EmailField(default='example@example.com' , null=False , blank=False , unique=True)
    username = models.CharField(max_length=255 , null=False , blank=False , unique=True) 
    is_active= models.BooleanField(default = True )
    is_verified= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return str(self.id) + '_' + str(self.username)


    class Meta:
        db_table = 'User'
        managed = True


class VerifyCode(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    code = models.IntegerField(default=0 , null=True , blank=True)
    email = models.EmailField(null=True , blank=True)
    is_expired = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + '_' + str(self.user.email)

    class Meta:
        db_table = 'VerifyCode'
        managed = True

class EmailConfig(models.Model):
    email_backend = models.CharField(
        max_length=64, default="django.core.mail.backends.smtp.EmailBackend"
    )
    email_host = models.CharField(max_length=64, default="smtp.gmail.com")
    email_port = models.IntegerField(default=587)
    Tls_value = models.BooleanField(default=True)
    email_host_user = models.EmailField(null=True, blank=True)
    email_host_password = models.CharField(max_length=200)
    Ssl_value = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) 
    class Meta:
        db_table = "Email_Confiq"



class TokenRecord(models.Model):
    token = models.CharField(max_length = 200, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'TokenRecord'
        managed = True

