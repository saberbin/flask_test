import jwt
from datetime import datetime, timedelta
import copy


def generate_jwt(payload, expiey=None, secret_key=None):
    _payload = copy.deepcopy(payload)
    if expiey is None:
        expiey = datetime.utcnow() + timedelta(hours=2)
    _payload.update({'exp': expiey})

    if secret_key is None:
        secret_key = 'qwerasdf'
    token = jwt.encode(_payload, secret_key, algorithm='HS256')
    return token.decode()


def verify_jwt(token):
    secret_key = 'qwerasdf'
    payload_data = None
    try:
        payload_data = jwt.decode(token, secret_key, algorithms='HS256')
    except Exception as e:
        print(e)

    return payload_data


if __name__ == '__main__':
    payload_data = {'user_name': 'Tom'}
    token = generate_jwt(payload_data)
    print(token)
    print(verify_jwt(token))
