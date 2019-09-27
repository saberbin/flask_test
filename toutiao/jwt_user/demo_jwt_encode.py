import jwt
from datetime import datetime, timedelta


payload_data = {
    'user_id': 1,
    'exp': datetime.utcnow() + timedelta(minutes=3)

}

secret_key = 'asiudhfPIUSHFPPIUWHFDE'
token = jwt.encode(payload_data, secret_key, algorithm='HS256')
print(token)
