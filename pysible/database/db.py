from .redis_client import redis_client

class Data:

    def load_role():
        try:
            redis_client.hset("role:root", mapping={"name": "root"})
            redis_client.hset("role:admin", mapping={"name": "admin"})
            redis_client.hset("role:editor", mapping={"name": "editor"})
            redis_client.hset("role:viewer", mapping={"name": "viewer"})
        except Exception as e:
            return {f"Failed to Load Role Data {e}"}
    
    def load_user():
        try:
            redis_client.hset(
            "user_id:DFU1",
            mapping={
                "username": "default_user",
                "password": "unique_password",
                "roles": ",".join(["root", "admin"])
            }
        )
        except Exception as e:
            return {f"Failed to load users {e}"}

    @staticmethod
    def load_data():
        """
        This will load some initially required data like
        roles - ["root", "admin", "user"]
        and dummy users- ["user1", "user2"]
        *** YOU CAN ADD OR REMOVE THIS DATA ANYTIME YOU WANT ***
        *** YOU CAN ADD NEW ROLES AND USERS ***
        """
        try:
            Data.load_role()
            Data.load_user()
            print("Added dafualt roles and user...")
        except Exception as e:
            return {f"Failed to run LOAD DATA Function {e}"}
        
    @staticmethod    
    def create_user(user_id: str, username: str, password: str, roles: list):
        for role in roles:
                if not redis_client.hgetall(f"role:{role}"):
                    print(f"⚠️ Please add {role} as a role first then try adding user. Use 'create_role()' for adding {role} as a role.")
                    return False
        if redis_client.keys(f"user_id:{user_id}"):
            print("⚠️ User_id is already taken. Please use something else...")
            return False
        try:
            redis_client.hset(
                f"user_id:{user_id}",
                mapping={
                    "username": username,
                    "password_hash": password,
                    "roles": ",".join(roles) 
                }
            )
            print("User saved in db ✅")
            return True
        except Exception as e:
            return {f"Failed to add new user ⚠️ {e}"}
    
    @staticmethod
    def create_role(role: str):
        if redis_client.keys(f"role:{role}"):
            print("⚠️ Role exists in db. No need to create one...")
            return False
        try:
            redis_client.hset(f"role:{role}", mapping={"name": f"{role}"})
            print("Role saved in db ✅")
            return True
        except Exception as e:
            raise e
