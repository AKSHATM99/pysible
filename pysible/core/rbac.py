from fastapi import Depends, HTTPException, status, Request
from pysible.database.redis_client import redis_client
from .token import Token
class RBAC:
    """
    class methods to deal with RBAC.
    Recieve "role" as a parameter and check with --> redis db
    """
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def require_user(request: Request):
        token = request.cookies.get("token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired Token.")
        payload = Token.decode_token(token=token)
        user_id: str = payload.get("user_id")
        return user_id
    
    @staticmethod
    def required_role(roles: list):
        def role_checker(cred_user_id: dict = Depends(RBAC.require_user)):
            for role in roles:
                if role in redis_client.hget(f"user_id:{cred_user_id}", "roles").decode().split(","):
                    return cred_user_id
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="Insufficient Permissions to Access this Endpoint")
        return role_checker