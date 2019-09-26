import jwt
from datetime import datetime, timedelta


payload_data = {
    'user_id': 1,
    'exp': datetime.utcnow() + timedelta(minutes=3)
}

secret_key = 'asiudhfPIUSHFPPIUWHFDE'
token = jwt.encode(payload_data, secret_key, algorithm='HS256')
print(token)

ret_data = jwt.decode(token.decode(), secret_key, algorithms='HS256')
print(ret_data)
