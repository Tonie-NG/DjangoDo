from rest_framework.response import Response
import jwt
from datetime import datetime, timedelta

def Sendresponse(status:bool, status_code:int, message:str, data=None):
    response = {
        "status": status,
        "status_code": status_code,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    return Response(response)

def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=5),
        'iat': datetime.utcnow()
    }

    access_token = jwt.encode(payload, 'secret', algorithm='HS256')

    return (access_token)
