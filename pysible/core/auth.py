from pysible.database.redis_client import redis_client
from fastapi.responses import JSONResponse
from .token import Token

class Auth:
    def __init__(self):
        pass
    
    @staticmethod
    def login(form_data):
        keys = redis_client.keys("user_id:*")
        user_ids = [key.decode().split("user_id:")[1] for key in keys]
        if form_data.username in user_ids:
            if form_data.password==redis_client.hget(f"user_id:{form_data.username}", "password").decode():
                access_token = Token.create_token(form_data.username, form_data.password)
                response = JSONResponse(content={"message": "Login Successful"})
                response.set_cookie(key="token", value=access_token, httponly=True)
                return response
            else:
                return "Wrong/Invalid Password !!!"
        else:
            return "User does not exists !!!"
        
    @staticmethod
    def logout():
        response = JSONResponse(content={"message": "Logged out successfully"})
        response.delete_cookie(key="token")
        return response
            