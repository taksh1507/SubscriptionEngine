# Code Overview and How to Run

This document explains what each file in the Subscription Microservice project does and how to run the project from scratch.

---

## File-by-File Explanation

### main.py
- **Purpose:** Entry point. Starts the FastAPI server.
- **How it works:**
  - Sets up the FastAPI app, CORS, and includes all API routes.
  - Run with: `python main.py`

### app/core/config.py
- **Purpose:** Loads configuration from `.env`.
- **How it works:**
  - Uses Pydantic to read environment variables (database URL, JWT secret, etc).
  - Makes these settings available to the rest of the app.

### app/db/base_class.py
- **Purpose:** Base class for all database models.
- **How it works:**
  - Ensures all models inherit common SQLAlchemy settings.

### app/db/session.py
- **Purpose:** Manages the database connection/session.
- **How it works:**
  - Sets up the SQLAlchemy engine and session.
  - Provides a `get_db()` function for use in API endpoints.

### app/models/subscription.py
- **Purpose:** Defines your database tables.
- **How it works:**
  - `Plan` model: describes subscription plans.
  - `Subscription` model: describes user subscriptions.

### app/schemas/subscription.py
- **Purpose:** Validates API input/output.
- **How it works:**
  - Uses Pydantic models to ensure data is correct for requests and responses.

### app/crud/subscription.py
- **Purpose:** Handles database operations (CRUD).
- **How it works:**
  - Functions to create, read, update, and delete plans and subscriptions.

### app/api/v1/endpoints/subscriptions.py
- **Purpose:** Defines the API endpoints.
- **How it works:**
  - Maps HTTP requests (POST, GET, PUT, DELETE) to CRUD functions.
  - Handles input validation and error responses.

### app/api/v1/api.py
- **Purpose:** Collects and organizes all API routes.
- **How it works:**
  - Includes the subscriptions endpoints under `/api/v1`.

### create_tables.py
- **Purpose:** Script to create all database tables.
- **How it works:**
  - Imports the models and runs `Base.metadata.create_all(bind=engine)` to create tables in your MySQL database.
  - Run with: `python create_tables.py`

---

## How to Run the Project

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Set up your `.env` file** (see `SETUP_AND_USAGE.md` for details).
3. **Create the MySQL database** (see `SETUP_AND_USAGE.md`).
4. **Create tables:**
   ```sh
   python create_tables.py
   ```
5. **Run the server:**
   ```sh
   python main.py
   ```
6. **Open your browser:**
   - Go to [http://localhost:8000/docs](http://localhost:8000/docs) to use the Swagger UI and test the API.

---

For more details, see `SETUP_AND_USAGE.md` and `README.md`. 