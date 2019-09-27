import jwt
from datetime import datetime, timedelta
import copy


def generate_jwt(payload, expiry=None, secret=None):
    _payload = copy.deepcopy(payload)
    if expiry is None:
        expiry = datetime.utcnow() + timedelta(hours=2)
    _payload.update({'exp': expiry})

    if secret is None:
        secret = 'qwerasfzxc'
    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token.decode()


def verify_jwt(token, secret=None):
    if secret is None:
        secret = 'qwerasfzxc'
    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
    except Exception as e:
        payload = None
    return payload


