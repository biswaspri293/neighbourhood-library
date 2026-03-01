# Neighborhood Library Service

A production-ready full-stack Library Management System built with:

-   **FastAPI (Python)**
-   **PostgreSQL**
-   **Next.js (React)**
-   **Docker**
-   **Pytest**

This project fulfills the requirements outlined in the take-home
specification and extends it with a minimal frontend for end-to-end
interaction.

------------------------------------------------------------------------

# 🚀 Features

## Core Functional Requirements

-   Create / Update / Delete Books
-   Create / Update / Delete Members
-   Borrow a Book
-   Return a Book
-   Query Borrowed Books (by member and status)
-   Enforced business rules (availability, uniqueness, active borrow
    constraints)

## Data Integrity & Validation

-   Unique (title, author) for books
-   Unique email for members
-   A member cannot borrow the same book twice while active
-   Available copies automatically updated on borrow/return
-   Proper HTTP status mapping (400 / 404 / 409)

------------------------------------------------------------------------

# 🏗 Architecture Overview

## Backend Structure

app/ \
    ├── routers/ # API route definitions\
    ├── services/ # Business logic layer\
    ├── models/ # SQL + schema definitions\
    ├── db.py # Connection handling\
    └── main.py # FastAPI entry point\
    |_____tests/ # Unit tests

### Design Principles

-   Clear separation of concerns (Router → Service → DB)
-   Explicit transaction management
-   Constraint-driven integrity at DB level
-   RESTful API design
-   Environment-driven configuration
-   Dockerized reproducible setup

------------------------------------------------------------------------

# 🗄 Database Schema Design

### books

-   id (PK)
-   title
-   author
-   total_copies
-   available_copies
-   created_at
-   UNIQUE(title, author)

### members

-   id (PK)
-   name
-   email (UNIQUE)
-   phone
-   created_at

### borrowings

-   id (PK)
-   member_id (FK → members.id)
-   book_id (FK → books.id)
-   borrowed_at
-   due_date
-   returned_at
-   status
-   UNIQUE(member_id, book_id) WHERE status = 'BORROWED'

Relationships: - One member → many borrowings - One book → many
borrowings

------------------------------------------------------------------------

# 🌐 Minimal Frontend (Next.js)

A minimal Next.js frontend is included to satisfy the requirement for a
web interface.

The frontend focuses on:

-   Form submission
-   Inline backend validation handling
-   Filtering and listing records
-   Borrow / Return operations

As my primary expertise is backend engineering, the UI is intentionally
minimal and functional rather than stylistically complex. The emphasis
was placed on correctness, API integration, and validation behavior
rather than advanced UX design.

------------------------------------------------------------------------

# ⚙ Environment Configuration

Create a `.env` file adding db configuration and api base url.

The `.env` file is excluded from version control.
`.env.example` added for reference. 

------------------------------------------------------------------------

# 🖥 Running Locally (Without Docker)

## 1. Create Virtual Environment

python3 -m venv venv\
source venv/bin/activate\
Clone repository - git clone https://github.com/biswaspri293/neighbourhood-library
## 2. Install Dependencies
cd backend\
pip install -r requirements.txt

## 3. Configure Environment

Create `.env` file with PostgreSQL connection string. And make sure your local postgres server is up and running on port 5432.

## 4. Run Backend

uvicorn app.main:app --reload

Access API Docs:

http://localhost:8000/docs

## 5. Run Frontend
Install node 18+ if not installed : https://nodejs.org \
####1.After installation, verify: 
node -v \
npm -v \
####2. Run app:
cd frontend\
npm run build \
npm start



------------------------------------------------------------------------

# 🐳 Running Using Docker (Recommended)

docker compose up --build

------------------------------------------------------------------------
#Access the platform using below links:
Backend Swagger/Api docs:

http://localhost:8000/docs

Frontend:

http://localhost:3000/

------------------------------------------------------------------------

# 🧪 Running Tests

pytest -v

With coverage:

pytest --cov=app --cov-report=term-missing

Tests isolate the database layer using mocks to ensure deterministic
execution.

------------------------------------------------------------------------

# 🤖 AI Usage Breakdown & Transparency

AI was used deliberately as a productivity accelerator and validation
assistant --- not as a substitute for architectural ownership.

## 1️⃣ Scaffolding & Boilerplate

AI assisted in:

-   Drafting service-layer structure
-   Creating Dockerfile and docker-compose scaffolding
-   Generating starter pytest test cases
-   Assisting with Next.js form structure and API integration patterns

All generated code was reviewed, refactored, and validated manually.

------------------------------------------------------------------------

## 2️⃣ Database & Transaction Validation

AI helped clarify:

-   psycopg transaction rollback behavior
-   Unique constraint handling patterns
-   Proper HTTP error translation
-   Edge-case handling scenarios

Final schema, constraints, and transaction strategy were designed and
implemented independently.

------------------------------------------------------------------------

## 3️⃣ Testing Strategy

AI assisted in:

-   Suggesting edge-case test coverage
-   Reviewing mocking patterns


All assertions, test structures, and business logic validation were
manually refined.

------------------------------------------------------------------------

## 4️⃣ Frontend Support

Given limited frontend experience, AI was used to:

-   Assist with form state handling
-   Improve error display logic
-   Structure API calls properly
-   Debug integration issues between frontend and backend

All integration behavior and validation handling were tested manually.

------------------------------------------------------------------------

## What AI Was NOT Used For

-   Blind generation of business logic
-   Architectural decision-making without review
-   Bypassing validation or testing rigor

All core service logic, schema design, transaction handling, and system
behavior were implemented and verified manually.

------------------------------------------------------------------------

# 🧠 Development Approach

-   Backend-first implementation
-   Strict validation and integrity rules
-   Explicit transaction handling
-   Clean service-layer separation
-   Dockerized environment
-   Automated test coverage
-   Minimal but functional frontend

------------------------------------------------------------------------

# 📈 Future Improvements

- Add authentication (JWT)
- Add pagination
- Introduce migrations (Alembic)
- Improve UI/UX design
- Add CI pipeline
- Improve logging

------------------------------------------------------------------------

# 👤 Author

Priyanka Biswas\
Senior Software Engineer
