# E-Commerce API

An educational project demonstrating a RESTful API for an e-commerce platform built with **FastAPI**, **SQLAlchemy** and **PostgreSQL**.  

This project implements basic e-commerce functionality: users, products, categories, reviews, and authentication using JWT tokens. Database migrations are handled with **Alembic**.

---

## Technologies

- **Python 3.14+**
- **FastAPI** – web framework
- **SQLAlchemy 2.0** – ORM
- **PostgreSQL** – database
- **Alembic** – migrations
- **PyJWT** – JWT authentication
- **python-dotenv** – environment variables
- **Uvicorn** – ASGI server

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kostasus/ecommerce_test_project.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Copy .env.example to .env and fill in your own values:
   ```bash
   cp .env.example .env
   ```

   Edit .env with your database URL and secret key:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
   SECRET_KEY=your-secret-key
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```
The API will be available at http://127.0.0.1:8000.

Interactive documentation at http://127.0.0.1:8000/docs.
