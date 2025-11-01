from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid
from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy

# def user_profile_upload_path(instance, filename):
#     return f"profile_pics/user_{instance.id}/{filename}"

def user_profile_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"profile_pics/{filename}"

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have a valid email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Super user must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super user must have is_superuser=True.")
        
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_customer = True
        user.is_seller = True
        
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # profile_pic = models.ImageField(
    #     upload_to=user_profile_upload_path,
    #     default="profile_pics/default_avatar.png",
    #     blank=True,
    #     null=True
    # )
    profile_pic = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        "Does the user have permission to view the app `app_lable`?"
        return self.is_superuser

    def save(self, *args, **kwargs):
        try:
            old = User.objects.get(pk=self.pk)
            if old.profile_pic and old.profile_pic != self.profile_pic:
                destroy(old.profile_pic.public_id)
        except User.DoesNotExist:
            pass  # First save, no old image
        super().save(*args, **kwargs)