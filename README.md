# Movie Review Platform

A web-based movie review application built with Python and Django. Users can explore movies, search and filter titles, submit temperature-based reviews, and track their reviewing activity through a personal dashboard.

## Features

### Movie Management
- Browse available movies.
- View detailed movie information.
- Search movies by title.
- Filter movies by genre.
- Sort movies alphabetically or by release order.
- Navigate movie listings using pagination.

### User Accounts
- User registration and login.
- User logout.
- Profile management.
- Update username, email, first name, and last name.
- Delete account functionality.

### Movie Reviews
- Create, view, edit, and delete reviews.
- Assign a temperature rating to movies.
- Prevent users from reviewing the same movie multiple times.
- Calculate and display audience temperature.

### Personal Dashboard
- View total reviews.
- View average review temperature.
- See personal review history.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| Django 6.1.2 | Web framework |
| PostgreSQL 17 | Relational database |
| Psycopg 3 | PostgreSQL database adapter |
| HTML5 | Web page structure |
| CSS3 | Web page styling |
| Django Templates | Dynamic HTML rendering |
| python-decouple | Environment variable management |

## Project Structure

```text
movie-review-platform/
│
├── accounts/          # User authentication and profiles
├── config/            # Django project configuration
├── dashboard/         # User dashboard and statistics
├── movies/             # Movie browsing and management
├── reviews/            # Movie review functionality
│
├── templates/          # HTML templates
├── static/             # CSS and static assets
│
├── .env.example        # Example environment configuration
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/JingJangRith/movie-review-platform.git
cd movie-review-platform
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure the following variables:

```env
SECRET_KEY=your_django_secret_key

DB_NAME=movie_review_db
DB_USER=postgres
DB_PASSWORD=your_local_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

Generate a Django secret key using:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key into your `.env` file.

**Important:** Never commit your `.env` file or expose your database password and secret key.

### 5. Create the PostgreSQL database

Create a PostgreSQL database named:

```text
movie_review_db
```

Make sure your PostgreSQL server is running and the database credentials match your `.env` configuration.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account (optional)

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

## Running Tests

Run the complete automated test suite:

```bash
python manage.py test
```

The project currently has **46 automated tests**, all passing in the latest verification.

## Database

This project uses PostgreSQL to store:

- User accounts
- Movie information
- Movie reviews
- Review ratings and related data

Database credentials are managed through environment variables.

## Development Notes

This project was developed as part of a Python II assignment.

The application is configured for local development. Additional production configuration, including deployment settings and security hardening, would be required before public deployment.

## Author

**Rith**

Computer Science Student

GitHub: [JingJangRith](https://github.com/JingJangRith)

---

*Movie Review Platform — Python II Assignment*