![Pysible Banner](static/banner2.png)
**<p align="center">📌 Pysible – Security Library for FastAPI</p>**

Pysible is an open-source security library for FastAPI applications.
It provides plug-and-play security features like authentication, authorization, API rate limiting, and logging with minimal boilerplate.

**Overview of Pysible (Recommended to Read)**
Pysible uses the 'Depends' functionality of FastAPI. When you install pysible and run `pysible action` from your desired location, pysible will create a connection with your running redis instance (using the host & port you provide) and create a new project folder with your chosen name (we will discuss this later in detail). Inside '/your_project_folder/src' you should create your FastAPI app. This is where you define all your business logic and API endpoints.
---

### Example: Protecting an Endpoint with JWT
Suppose you have an endpoint "/index" in your FastAPI app. You want only authenticated users with a valid JWT to access this endpoint. In that case, you can use the `RBAC.require_token` dependency from Pysible:

```python
from fastapi import FastAPI, Depends
from pysible.core import RBAC

app = FastAPI()

@app.get("/index")
async def my_func(user = Depends(RBAC.require_token)):
    return {"message": "Only users with valid JWT can access this endpoint."}

# This example only demonstrates how to protect an endpoint using Pysible’s RBAC (JWT).
# In practice, clients must first obtain a JWT via the login functionality
# before they can access protected endpoints.
# This code provides you the rough idea of how to use jwt based authentication in your endpoints.
# Later on we will discuss everything in detail.
```

---
👉 Install directly from PyPI: 

```python
pip install pysible
```

---
🚀 Features:

🔑 JWT Authentication – Easy login/logout with token-based security.

🛡 RBAC (Role-Based Access Control) – Fine-grained access control for endpoints. ** requires Redis **

⚡ API Rate Limiting – Protect APIs from abuse using Redis-powered rate limiting. ** requires Redis **

📝 Logging System – Store logs at different levels (INFO, DEBUG, ERROR, etc.) in files for better observability.

⚙️ Plug-and-Play – Import features and add to endpoints via FastAPI’s Depends.

---
👉**Now follow this docs step-by-step from this point for better understanding**

🔧 **Usage**

After installing pysible, from your desired directory run --> ( in your terminal/powershell )
```
pysible action
```
This will ask for few terminal based prompt like ->
```python
Project Name:->:
Redis is running now? (yes/no):->:
Host of Redis (e.g 'localhost' if running locally):->:
Port of Redis:->:
Redis DB Number (e.g '0', '1'):->:
Do you want to load dummy data for testing? (yes/no):
Do you want to set your own secret key? (yes/no):
```
---
⚠️ **Important Note** 

Pysible requires a **running Redis instance** on your machine.  
It will automatically try to connect with redis using the provided **Redis HOST** and **PORT**.  
 
If Pysible is unable to connect to Redis, you may encounter errors such as:  
```
❌ redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```
```
✅ Make sure Redis is installed and running before starting your FastAPI app with Pysible.
```

**( Optional but recommended )**

1- Pysible gives you the option to load dummy data into your redis db for testing purpose.<br/>

2- While not required, this step provides a ready-to-use setup so you can start experimenting immediately—no need to define custom users or roles upfront.<br/>

3- Dummy Data Format-<br/>
```
Default User - { "user_id : "root",
                    "password : "unique_password",
                    "roles: : ["root", "admin"]
                    }

Default Roles - "role:root", mapping={"name": "root"}
                "role:admin", mapping={"name": "admin"}
                "role:editor", mapping={"name": "editor"}
                "role:viewer", mapping={"name": "viewer"}
```
3- It is recommended to set a "UNIQUE_SECRET_KEY" otherwise you will get a warning "SECRET_KEY must be set in 'Production' ! Please configure it as an environment variable.".

---
📂 Project Structure (Example): If everything goes well, Pysible will make this for you.
```
my_fastapi_app/                  # Your FastAPI project
│── src/                         # Create your endpoints and main.py in this directory
│
│── static/                      # Optional: static files (images, docs, assets)
│
│── tests/                       # Test cases for your app
│
│── requirements.txt             # Project dependencies
│── .env                         # Environment variables (Redis HOST, PORT, JWT secret, etc.)
│── README.md                    # Project documentation
│── .gitignore                   # Ignore venv, cache, logs
│── LICENSE                      # License file (if open source)
```
---


**ℹ️There are 3 main functionalities in Pysible.**

```python
│── core/          # Authentication, rate limiting, JWT handling and RBAC.
│
│── database/      # Manage users and roles using the Redis client.
│
│── logger/        # Universal logger for writing events to a separate log file.
```


***ℹ️How to use Pysible Features in your Endpoints**

*We’ll start with the most basic features — login and logout — and then gradually cover advanced functionalities step by step.*

1. **Login/Logout**

```python
from fastapi import FastAPI, Depends 
from fastapi.security import OAuth2PasswordRequestForm
from pysible.core import Auth

app = FastAPI()

@app.post("/login")
async def login_func(form_data: OAuth2PasswordRequestForm = Depends()):
    return Auth.login(form_data=form_data)

@app.get("/logout")
async def logout_func():
    return Auth.logout()
```

In the above code snippet, the Auth class is imported from pysible.core.
Inside our /login endpoint, we use OAuth2PasswordRequestForm = Depends() because we expect the client to send a username (user_id) and password through a form.

You can easily test this using the built-in Swagger/OpenAPI UI by visiting /docs.

In the endpoint’s return statement, we call Auth.login(form_data), where form_data contains the submitted user_id and password.

👉 For testing purposes, you can log in with the following default credentials:

*Username* (user_id): root

*Password*: unique_password


2. **JWT Based Authentication**:
*JWT comes from RBAC in pysible.*
```python

from fastapi import FastAPI, Depends 
from fastapi.security import OAuth2PasswordRequestForm
from pysible.core import Auth, RBAC  # import RBAC

app = FastAPI()

@app.post("/login")
def login_func(form_data: OAuth2PasswordRequestForm = Depends()):
    return Auth.login(form_data=form_data)

# Pass RBAC.require_token as a dependecy in your endpoint.
# If user is authenticated then only user is allowed to access this endpoint.

@app.get("/secure_route", user = Depends(RBAC.require_token))
def secure_endpoint():
    return {"This is a secure endpoint."}

@app.get("/logout")
def logout_func():
    return Auth.logout()
```

3. **Role Based Access Control (RBAC)**:
*You can pass the list of `specific` allowed roles to the endpoints. Only users with `atleast one` allowed role/roles can access this endpoint.* 

```python
from fastapi import FastAPI, Depends 
from fastapi.security import OAuth2PasswordRequestForm
from pysible.core import Auth, RBAC  # import RBAC

app = FastAPI()

@app.post("/login")
async def login_func(form_data: OAuth2PasswordRequestForm = Depends()):
    return Auth.login(form_data=form_data)

# Pass the list of allowed of roles in the endpoint as an dependency.
# If authenticated user has atleast one role from the list of allowed roles then only user is allowed to access this endpoint.

@app.get("/secure_route", user = Depends(RBAC.require_token), role = Depends(RBAC.require_role(["root",      "admin", "manager"])))

async def secure_endpoint():
    return {"This is a secure endpoint."}

@app.get("/logout")
async def logout_func():
    return Auth.logout()
```

4. **Rate Limiting**:
*Rate Limiting restricts the number of times an endpoint can be called or accessed within a defined time window.*
*It is a crucial feature in modern web applications as it helps protect your app and resources from excessive requests, unusual traffic spikes, or automated bot attacks.*
```python

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pysible.core import Auth, RBAC, PyRate # import `PyRate` from pysible

app = FastAPI()

@app.post("/login")
async def login_func(form_data: OAuth2PasswordRequestForm = Depends()):
    return Auth.login(form_data=form_data)

# PyRate.rate_limiter(1, 5) means that this endpoint can be accessed 1 time per second, with a burst window capacity of 5.
# The first number (1) represents the allowed requests per second.
# The second number (5) represents the size of the burst window (the temporary extra capacity allowed during short traffic spikes).

# You can change these values as per your needs.

@app.get("/secure_route", user = Depends(RBAC.require_token), role = Depends(RBAC.require_role(["root",      "admin", "manager"])), rate =  Depends(PyRate.rate_limiter(1, 5)))

async def secure_endpoint():
    return {"This is a secure endpoint."}

@app.get("/logout")
async def logout_func(user_id: str = Depends(RBAC.require_token)):
    return Auth.logout(user_id)

```

5. **Addtional Info**
*If you want, you can pass all or multiple dependecies together as shown below:
```python
@app.get("/secure_route", dependencies=[
                        Depends(RBAC.require_role(["ROOT", "admin"])), #case-sensitivity doesn’t apply here
                        Depends(RBAC.require_token),
                        Depends(PyRate.rate_limiter(1, 5))],)
async def secure_endpoint():
    return {"This is a secure endpoint."}
```
✨ This endpoint has multiple dependencies. It can only be accessed if:

1- The user is authenticated and has a valid JWT.
2- The user has at least the root or admin role.
3- The number of requests is within the allowed limit (1 request/second in this case).

✅ Only when all three conditions are satisfied, access to this endpoint is granted.

6. **Universal Logger**
*By default you will the important logs of your app in `/logs/app.log` file.*

*Sample Logs*
```python

2025-09-16 01:16:36,025 - INFO - User 'root' logged in successfully.
2025-09-16 01:16:46,407 - WARNING - 'Unauthorized' access attempt | User: 'root' | Endpoint: '/secure_route'
2025-09-16 01:36:41,741 - WARNING - 'Too many requests' to endpoint: '/health'
2025-09-16 01:36:41,916 - WARNING - 'Too many requests' to endpoint: '/health'
2025-09-16 00:58:50,585 - INFO - User 'root' logged out successfully.

```
---

***Database related features/opreations:***
1. **Add users in db by using redis_client->**
