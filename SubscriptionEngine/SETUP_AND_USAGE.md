# Setup and Usage Guide

This guide will help you set up, run, and understand the SubscriptionEngine project.

---

## 1. Prerequisites
- **Python 3.8+** installed
- **MySQL** installed and running

---

## 2. Project Setup

### a. Clone the Repository
```
git clone <your-repo-url>
cd <project-directory>
```

### b. Install Dependencies
```
pip install -r requirements.txt
```

### c. Configure Environment Variables
Create a `.env` file in the project root with the following content:
```
DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:3306/subscription_db
JWT_SECRET_KEY=<your-secret-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
- Replace `<username>` and `<password>` with your MySQL credentials.
- Replace `<your-secret-key>` with a secure random string.

### d. Create the Database
- Open MySQL and run:
  ```sql
  CREATE DATABASE subscription_db;
  ```
  (Or use a different name and update `.env` accordingly)

### e. Create Database Tables
```
python create_tables.py
```

---

## 3. Running the Application
```
python main.py
```
- The server will start on `http://0.0.0.0:8000` (access via `http://localhost:8000`)

---

## 4. API Usage

### a. Open Swagger UI
- Go to [http://localhost:8000/docs](http://localhost:8000/docs)
- You can test all endpoints interactively here.

### b. Example API Calls

#### Create a Plan
- **POST /api/v1/plans/**
- Example body:
  ```json
  {
    "name": "Pro",
    "price": 19.99,
    "features": "Unlimited access, Priority support",
    "duration_days": 30
  }
  ```

#### List All Plans
- **GET /api/v1/plans/**

#### Subscribe a User
- **POST /api/v1/subscriptions/**
- Example body:
  ```json
  {
    "user_id": 1,
    "plan_id": 2
  }
  ```

#### Get User Subscription
- **GET /api/v1/subscriptions/{user_id}**

#### Update Subscription
- **PUT /api/v1/subscriptions/{user_id}**
- Example body:
  ```json
  {
    "plan_id": 3
  }
  ```

#### Cancel Subscription
- **DELETE /api/v1/subscriptions/{user_id}**

---

## 5. How It Works
- The app loads config from `.env` using Pydantic.
- Connects to MySQL using SQLAlchemy.
- API endpoints are available for plans and subscriptions.
- Use Swagger UI for easy testing.

---

## 6. Extending the Project
- Add authentication endpoints for user login/signup.
- Add background jobs for auto-expiring subscriptions.
- Add admin endpoints for plan management.
- Write tests using `pytest`.

---

## 7. Troubleshooting
- **Can't connect to MySQL?** Check your credentials and that MySQL is running.
- **.env errors?** Make sure the file exists and is in the project root.
- **Port in use?** Change the port in `main.py` if needed.

---

For any issues, check the logs or ask for help! 