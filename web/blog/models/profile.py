from django.db import models
import os
import uuid

from .user import User

def user_profile_pic_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}" 
    return f'profile_pic/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=70, null=True, blank=True)
    last_name = models.CharField(max_length=70, null=True, blank=True)
    about = models.CharField(max_length=150, null=True, blank=True)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)