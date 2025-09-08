from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "dev_only_secret"
ALGORITHM = "HS256"
ACCESS_EXPIRE_MIN = 30

class Token:
    def __init__(self):
        pass
    
    @staticmethod
    def create_token(user_id: str, password: str):
        expire = datetime.now() + timedelta(minutes=ACCESS_EXPIRE_MIN)
        to_encode = {"user_id": user_id, "password": password, "exp": expire}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def decode_token(token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return None