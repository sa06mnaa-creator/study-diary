from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager

from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    birthday = models.DateField(null=False, blank=False)

    objects = UserManager()

class UserActivateTokenManager(models.Manager):
    
    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=timezone.now()
        ).first()
        if not user_activate_token:
            raise ValueError('トークンが存在しません')
        
        user = user_activate_token.user
        user.is_active = True
        user.save()
        return user

    def create_or_update_token(self, user):
        token = str(uuid4()) #トークンの発行
        exired_at = timezone.now() + timedelta(days=1) # トークンの期限（1日後）　
        user_token, created =self.update_or_create(
            user=user,
            defaults={'token': token, 'expired_at': exired_at,}

        )
        return user_token
class UserActivateToken(models.Model):
    token = models.UUIDField(db_index=True, unique=True)
    expired_at = models.DateTimeField()
    user = models.OneToOneField(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='user_activate_token'
    )

    objects = UserActivateTokenManager()

    class Meta:
        db_table = 'user_activate_token'

@receiver(post_save, sender=CustomUser)
def publish_token(sender, instance,created, **kwargs):
    user_activate_token = UserActivateToken.objects.create_or_update_token(instance)
    print(
        f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}'
        )
# Create your models here.



        
         