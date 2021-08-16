from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customers(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=250, null=True)
    email_otp = models.IntegerField(null=True)
    email_verified = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=250, null=True)
    auth_token = models.CharField(max_length=250, null=True)
    customer_status = models.CharField(
        max_length=250, default='active', null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username


class Intents(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True)
    tag = models.CharField(max_length=250, null=True)
    patterns = models.TextField(null=True)
    responses = models.TextField(null=True)
    render_status = models.CharField(max_length=250, default='raw', null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.tag
