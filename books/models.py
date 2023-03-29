from django.db import models
from users.models import User
import os
import uuid
from cloudinary.models import CloudinaryField
# Create your models here.

def get_avatar_upload_path(instance, filename):
    return os.path.join("books/cover_image/{}/{}".format(instance.title, filename))


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=True, unique=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="users_books")
    doc = models.FileField(upload_to="File/books", null=True)
    thumbnail = models.ImageField(null=True, upload_to=get_avatar_upload_path)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="users_subscription")
    trans_ref = models.CharField(max_length=255, null=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
