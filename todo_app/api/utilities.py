from rest_framework.response import Response

def Sendresponse(status:bool, status_code:int, message:str, data=None):
    response = {
        "status": status,
        "status_code": status_code,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    return Response(response)
