# 🚀 SubscriptionEngine  

SubscriptionEngine is a robust and flexible service designed to manage user subscriptions for SaaS platforms. Built using FastAPI and MySQL, it provides a modular architecture, secure authentication, and comprehensive subscription management features.

## ✨ Key Features

*   📋 User subscription management (create, retrieve, update, cancel)
*   💰 Subscription plan management
*   📊 Subscription status tracking (ACTIVE, INACTIVE, CANCELLED, EXPIRED)
*   🔐 JWT-based authentication
*   🧩 Clean, modular codebase
*   ⚙️ Environment-based configuration
*   ✅ Input/output validation with Pydantic
*   📖 Auto-generated Swagger UI for API testing

## 🎯 Features
- 👤 User subscription management (create, retrieve, update, cancel)
- 📦 Subscription plan management
- 📈 Subscription status tracking (ACTIVE, INACTIVE, CANCELLED, EXPIRED)
- 🔑 JWT-based authentication (ready for extension)
- 🏗️ Clean, modular codebase using FastAPI and SQLAlchemy
- 🌍 Environment-based configuration
- ✔️ Input/output validation with Pydantic
- 🎨 Auto-generated Swagger UI for API testing

## 🛠️ Tech Stack
- **Backend:** 🐍 Python (FastAPI)
- **Database:** 🗄️ MySQL (SQLAlchemy ORM)
- **Authentication:** 🔒 JWT (extendable)
- **Config:** 📄 .env + Pydantic BaseSettings

## 🚀 Setup Instructions

### 1. 📥 Clone the Repository
```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. ⚙️ Configure Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:3306/subscription_db
JWT_SECRET_KEY=<your-secret-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. 🗄️ Create the Database
- Ensure MySQL is running
- Create a database named `subscription_db` (or update the name in `.env`)

### 5. 🏗️ Create Database Tables
```bash
python create_tables.py
```

### 6. ▶️ Run the Application
```bash
python main.py
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) 📖 for the Swagger UI.

---

## 📚 API Documentation

### 💰 Plans
- **POST /api/v1/plans/**
  - ➕ Create a new subscription plan
  - **Body:**
    ```json
    {
      "name": "Pro",
      "price": 19.99,
      "features": "Unlimited access, Priority support",
      "duration_days": 30
    }
    ```
- **GET /api/v1/plans/**
  - 📋 Retrieve all available plans

### 📋 Subscriptions
- **POST /api/v1/subscriptions/**
  - ➕ Create a new subscription for a user
  - **Body:**
    ```json
    {
      "user_id": 1,
      "plan_id": 2
    }
    ```
- **GET /api/v1/subscriptions/{user_id}**
  - 🔍 Retrieve a user's active subscription
- **PUT /api/v1/subscriptions/{user_id}**
  - ✏️ Update a user's subscription (e.g., change plan)
  - **Body:**
    ```json
    {
      "plan_id": 3
    }
    ```
- **DELETE /api/v1/subscriptions/{user_id}**
  - ❌ Cancel a user's subscription

---

## 📁 Project Structure
```
.
├── app
│   ├── api
│   │   └── v1
│   │       ├── api.py
│   │       └── endpoints
│   │           └── subscriptions.py
│   ├── core
│   │   └── config.py
│   ├── crud
│   │   └── subscription.py
│   ├── db
│   │   ├── base_class.py
│   │   └── session.py
│   ├── models
│   │   └── subscription.py
│   └── schemas
│       └── subscription.py
├── create_tables.py
├── main.py
├── requirements.txt
└── .env
```

## 🔮 Extending & Maintenance
- 🔐 Add authentication endpoints for user login/signup
- ⏰ Integrate background jobs for auto-expiring subscriptions
- 👨‍💼 Add admin endpoints for plan management
- 🧪 Write unit/integration tests (pytest recommended)