# ![Pysible Banner](static/banner2.png)

<p align="center"><b>📌 Pysible – Security Library for FastAPI</b></p>

Pysible is an **open-source security library** for [FastAPI](https://fastapi.tiangolo.com/) applications.  
It provides **plug-and-play** security features like authentication, authorization, API rate limiting, and logging — all with minimal boilerplate.  

---

## 🚀 Features
- 🔑 **JWT Authentication** – Simple login/logout with token-based security.  
- 🛡 **RBAC (Role-Based Access Control)** – Fine-grained access control for endpoints. *(requires Redis)*  
- ⚡ **API Rate Limiting** – Redis-powered rate limiting to protect your APIs. *(requires Redis)*  
- 📝 **Logging System** – Store logs at different levels (`INFO`, `DEBUG`, `ERROR`, etc.) for observability.  
- ⚙️ **Plug-and-Play** – Import features and attach them to endpoints using FastAPI’s `Depends`.  

👉 Install directly from PyPI:  
```bash
pip install pysible
```

---

## 📖 Overview
Pysible is built on top of FastAPI’s `Depends` functionality.  

When you install `pysible` and run:  
```bash
pysible action
```
It will:
1. Connect to your running **Redis instance** (you provide host & port).  
2. Generate a new project folder with your chosen name.  
3. Inside `/your_project_folder/src` → You’ll build your FastAPI app (business logic + endpoints).  

---

## 🛠 Usage
After installing, from your desired directory run:  
```bash
pysible action
```

You’ll be prompted for setup:
```text
Project Name:->:
Redis is running now? (yes/no):->:
Host of Redis (e.g. 'localhost'):->:
Port of Redis:->:
Redis DB Number (e.g. '0', '1'):->:
Do you want to load dummy data for testing? (yes/no):
Do you want to set your own secret key? (yes/no):
```

---

## ⚠️ Important Note
Pysible **requires a running Redis instance**.  
It automatically connects using the provided host & port.  

If Redis isn’t running, you may see:
```
❌ redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```

✅ Make sure Redis is installed and running before starting your FastAPI app with Pysible.  

---

## 📦 Project Structure (Generated Example)
If setup completes successfully, you’ll get:
```
my_fastapi_app/                  # Your FastAPI project
│── src/                         # Create your endpoints & main.py here
│── static/                      # Optional: static files (images, docs, assets)
│── tests/                       # Test cases
│── requirements.txt             # Dependencies
│── .env                         # Environment variables (Redis HOST, PORT, JWT secret, etc.)
│── README.md                    # Project documentation
│── .gitignore                   # Ignore venv, cache, logs
│── LICENSE                      # License file
```

---

## 🧩 Core Modules
```
│── core/          # Authentication, rate limiting, JWT handling, RBAC
│── database/      # Manage users and roles with Redis
│── logger/        # Universal logger (writes events to /logs/app.log)
```

---

## ✨ Step-by-Step Guide

### 1. Login / Logout
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

👉 Test easily using Swagger UI (`/docs`).  
Default credentials (if dummy data loaded):  
- **Username**: `root`  
- **Password**: `unique_password`  

---

### 2. JWT Authentication
```python
from fastapi import FastAPI, Depends 
from fastapi.security import OAuth2PasswordRequestForm
from pysible.core import Auth, RBAC

app = FastAPI()

@app.post("/login")
def login_func(form_data: OAuth2PasswordRequestForm = Depends()):
    return Auth.login(form_data=form_data)

@app.get("/secure_route", user=Depends(RBAC.require_token))
def secure_endpoint():
    return {"This is a secure endpoint."}

@app.get("/logout")
def logout_func():
    return Auth.logout()
```

---

### 3. Role-Based Access Control (RBAC)
```python
from fastapi import FastAPI, Depends 
from fastapi.security import OAuth2PasswordRequestForm
from pysible.core import Auth, RBAC

app = FastAPI()

@app.post("/login")
async def login_func(form_data: OAuth2PasswordRequestForm = Depends()):
    return Auth.login(form_data=form_data)

@app.get("/secure_route", 
         user=Depends(RBAC.require_token), 
         role=Depends(RBAC.require_role(["root", "admin", "manager"])))
async def secure_endpoint():
    return {"This is a secure endpoint."}

@app.get("/logout")
async def logout_func():
    return Auth.logout()
```

---

### 4. Rate Limiting
```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pysible.core import Auth, RBAC, PyRate

app = FastAPI()

@app.post("/login")
async def login_func(form_data: OAuth2PasswordRequestForm = Depends()):
    return Auth.login(form_data=form_data)

@app.get("/secure_route",
         user=Depends(RBAC.require_token),
         role=Depends(RBAC.require_role(["root", "admin", "manager"])),
         rate=Depends(PyRate.rate_limiter(1, 5)))
async def secure_endpoint():
    return {"This is a secure endpoint."}

@app.get("/logout")
async def logout_func(user_id: str = Depends(RBAC.require_token)):
    return Auth.logout(user_id)
```

Here:  
- `1` = requests allowed per second  
- `5` = burst window (extra capacity allowed during spikes)  

---

### 5. Multiple Dependencies Together
```python
@app.get("/secure_route", dependencies=[
    Depends(RBAC.require_role(["root", "admin"])),
    Depends(RBAC.require_token),
    Depends(PyRate.rate_limiter(1, 5))])
async def secure_endpoint():
    return {"This is a secure endpoint."}
```

✅ Access granted only if:  
1. User has a valid JWT.  
2. User has at least one allowed role (`root`/`admin`).  
3. Request rate is within the allowed limit.  

---

### 6. Universal Logger
Logs are stored in `/logs/app.log`.  

**Sample Output**:
```text
2025-09-16 01:16:36,025 - INFO - User 'root' logged in successfully.
2025-09-16 01:16:46,407 - WARNING - 'Unauthorized' access attempt | User: 'root' | Endpoint: '/secure_route'
2025-09-16 01:36:41,741 - WARNING - 'Too many requests' to endpoint: '/health'
2025-09-16 00:58:50,585 - INFO - User 'root' logged out successfully.
```

---

## 🗄 Database Operations
Pysible uses Redis to manage users & roles.  
Example: adding users directly via the Redis client.  

---

## ✅ Summary
Pysible provides a **ready-to-use security toolkit** for FastAPI:  
- Authentication (JWT)  
- Authorization (RBAC)  
- Rate Limiting  
- Centralized Logging  

With just a few lines of code, you can secure endpoints and scale safely 🚀  

---
