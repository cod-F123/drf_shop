from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random
from datetime import timedelta

# Create your models here.


class UserManager(BaseUserManager):
    
    def create_user(self, phone, password=None, **extra_fields):
        
        if not phone:
            raise ValueError(_("User must have an phone number"))
        
        user = self.model(phone = phone, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, phone,  password=None, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    """ This class defines the user model """

    phone = models.CharField(_("phone_number"),max_length=13, unique=True)
    email = models.EmailField(_("email"), max_length=255, unique=True, blank=True, null=True)

    is_active = models.BooleanField(verbose_name=_("is active"), default=True)
    is_staff = models.BooleanField(verbose_name=_("is staff"), default=False)
    is_superuser = models.BooleanField(
        verbose_name=_("is superuser"), default=False
    )
    is_verified = models.BooleanField(
        verbose_name=_("is verified"), default=False
    )

    created_date = models.DateTimeField(
        verbose_name=_("created date"), auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_("updated_date"), auto_now=True
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone
    

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.phone 
    

class OtpCode(models.Model):
    
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    otp_code = models.CharField(max_length=6,blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(blank=True, null=True)

    can_try_times = models.IntegerField(default=3)

    @property
    def is_expired(self):
        return self.expired_at < timezone.now()
    
    def save(self, *args, **kwargs):

        if self.otp_code is None:
            self.otp_code = random.randint(100000,999999)
            self.expired_at = timezone.now() + timedelta(minutes=2)
    
        super().save(*args, **kwargs)

class AddressUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

    title = models.CharField(max_length=155)
    address = models.TextField()
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.phone