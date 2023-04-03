from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_soft_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if self.is_soft_deleted and self.user.is_active:
            self.user.is_active = False
            self.user.save()
        super().save(*args, **kwargs)