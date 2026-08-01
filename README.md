# SubscriptionEngine

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

SubscriptionEngine is a robust, production-ready microservice designed to manage user subscriptions for SaaS platforms. Built using FastAPI and SQLAlchemy, it provides a modular architecture, secure authentication, and comprehensive subscription management features.

---

## Table of Contents
- [Key Features](#key-features)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Getting Started](#getting-started)
  - [Running with Docker (Recommended)](#running-with-docker-recommended)
  - [Running Locally (Manual Setup)](#running-locally-manual-setup)
- [Testing](#testing)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)

---

## Key Features

- **User Management & Auth:** User registration, secure bcrypt password hashing, and JWT-based authentication.
- **Role-Based Access Control (RBAC):** Secure endpoints ensuring users can only manage their own data, while only administrators can configure plans.
- **Subscription Lifecycle:** Full support for creating, retrieving, updating, upgrading, and cancelling subscriptions.
- **Advanced Billing Logic:** Plan upgrades and downgrades automatically recalculate and reset the billing cycle. Cancellations utilize a `cancel_at_period_end` flag instead of immediately terminating access.
- **Data Integrity:** Soft deletes (`is_deleted` flags) are implemented across models to prevent destructive hard deletions.
- **Pagination:** Standardized `PaginatedResponse` wrappers are used for all list endpoints to ensure optimal performance.
- **Background Processing:** Integrated `APScheduler` runs background jobs to automatically transition expired subscriptions to an `EXPIRED` state.
- **Robust Error Handling:** Global exception handlers guarantee standardized JSON error responses across the entire application.
- **Database Migrations:** Fully configured with `Alembic` for safe and trackable schema evolution.

---

## Architecture & Tech Stack

| Component | Technology |
|---|---|
| **Web Framework** | Python 3.11, FastAPI |
| **Database** | SQLite (development) / MySQL (production ready) |
| **ORM** | SQLAlchemy 2.0 |
| **Migrations** | Alembic |
| **Authentication** | JWT, passlib (bcrypt) |
| **Task Scheduler** | APScheduler |
| **Testing** | Pytest, HTTPX |

---

## Getting Started

### Running with Docker (Recommended)

The easiest way to initialize the application is by using Docker Compose, which handles all dependencies and environment configurations automatically.

```bash
git clone <your-repo-url>
cd SubscriptionEngine
docker-compose up --build
```

> **Note:** The API will be immediately available at `http://localhost:8000`. You can access the interactive Swagger documentation at `http://localhost:8000/docs`.

### Running Locally (Manual Setup)

#### 1. Install Dependencies
Ensure you have Python 3.11+ installed, then install the required packages:
```bash
pip install -r requirements.txt
```

#### 2. Configure Environment Variables
Create a `.env` file in the project root directory. By default, the application will use a local SQLite database for ease of development:
```env
DATABASE_URL=sqlite:///./subscription_db.db
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
> To use MySQL in production, update the `DATABASE_URL` format to: `mysql+pymysql://<user>:<password>@<host>:<port>/<db_name>`

#### 3. Run Database Migrations
Initialize the database schema using Alembic:
```bash
python -m alembic upgrade head
```

#### 4. Start the Application
Launch the Uvicorn server:
```bash
python main.py
```

---

## Testing

The repository includes a comprehensive test suite using `pytest`. The tests execute against an isolated in-memory SQLite database, ensuring that your development data remains untouched.

To run the test suite:
```bash
python -m pytest -v
```

---

## API Reference

Below is a summary of the core endpoints. For the complete, interactive API documentation, visit the `/docs` endpoint while the server is running.

### Authentication & Users
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/users/` | Register a new user account |
| `POST` | `/api/v1/login/access-token` | Authenticate and retrieve a JWT bearer token |

### Subscription Plans
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/plans/` | Create a new subscription plan *(Admin Only)* |
| `GET` | `/api/v1/plans/` | Retrieve a paginated list of available plans |

### Subscriptions
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/subscriptions/` | Subscribe a user to a specific plan |
| `GET` | `/api/v1/subscriptions/{user_id}` | Retrieve a user's active subscription details |
| `PUT` | `/api/v1/subscriptions/{user_id}` | Update or upgrade a user's subscription |
| `DELETE`| `/api/v1/subscriptions/{user_id}` | Cancel a subscription (schedules for period end) |

---

## Project Structure

```text
SubscriptionEngine/
├── alembic/                # Database migration scripts and versions
├── app/
│   ├── api/                # API routers, endpoints, and dependencies
│   ├── core/               # Application configuration, security, and task schedulers
│   ├── crud/               # Database CRUD operations
│   ├── db/                 # Database session setup and declarative base
│   ├── models/             # SQLAlchemy ORM definitions
│   └── schemas/            # Pydantic validation and serialization schemas
├── tests/                  # Pytest unit and integration test suites
├── .env                    # Environment configuration file
├── alembic.ini             # Alembic configuration
├── docker-compose.yml      # Docker compose deployment configuration
├── Dockerfile              # Docker image definition
├── main.py                 # FastAPI application entry point
└── requirements.txt        # Python package dependencies
```

---

## Contributing

Contributions are always welcome! If you'd like to help improve SubscriptionEngine, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.