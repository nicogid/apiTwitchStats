from datetime import datetime, timedelta
import hashlib
from .models import AccessToken


def create_token(user):
    access_token = AccessToken(user=user, expiration_date=datetime.now() + timedelta(hours=2))
    access_token.token = hashlib.md5((str(access_token.expiration_date) + str(user)).encode('utf-8')) \
        .hexdigest()
    access_token.save()
    return access_token
