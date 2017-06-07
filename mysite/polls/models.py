from django.utils import timezone
import datetime

from django.db import models

def get_expiration_date():
    return timezone.now() + datetime.timedelta(day=1)

class Token(models.Model):
    user = models.OneToOneField('auth.User',on_delete=models.CASCADE,unique=True)
    hash = models.CharField(max_length=100)
    expiration_date = models.DateTimeField(default=get_expiration_date)

    def is_expired(self):
        return self.expiration_date < timezone.now()
