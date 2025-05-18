# Notification-Service

A real-time in-app notification system built using FastAPI and WebSockets. Notifications are stored in a PostgreSQL database and delivered instantly through a responsive frontend interface.

## Features

- Real-time notifications using WebSocket
- Fetch and display notifications by user ID
- Responsive UI using Tailwind CSS
- Jinja2 templating with WebSocket integration
- REST API for creating and retrieving notifications
- Swagger UI for API docs and testing

## Tech Stack

- **FastAPI:** Web Framework
- **PostgreSQL:** Storing notification data
- **SQLAlchemy:** ORM for database management
- **Pydantic:** Used for data validation
- **WebSockets:** For real-time notification delivery
- **Jinja2:** HTML templating engine
- **Tailwind CSS:** Frontend styling

## Prerequisites

- **Python** installed on the system
- **PostgreSQL** set up and running on the system
- **Git** for version control

## Setup

### 1️. Clone the Project

`git clone https://github.com/Neelu2647/Notification-Service
cd Notification-Service`

### 2️. Create a Virtual Environment
`python -m venv venv
source venv/bin/activate `

### 3️. Install Dependencies
`pip install -r requirements.txt`

### Database Setup
Start PostgreSQL service and create a database named notificationdb:

`psql -U postgres`

`postgres=# CREATE DATABASE notificationdb;`
`CREATE DATABASE`

`postgres=# CREATE USER <username> WITH PASSWORD '<password>';`
`CREATE ROLE`

`postgres=# GRANT ALL PRIVILEGES ON DATABASE notificationdb TO <username>;`
`GRANT`

### Environment Variables
Create a .env file in the project root with the following:

`DATABASE_URL = "postgresql+asyncpg://neondb_owner:<username>/neondb?ssl=require"`

### Run Locally

`uvicorn app.main:app --reload`
By default, it will run on: `http://127.0.0.1:8000`

### Usage
# 🌐 Web Interface

Navigate to http://127.0.0.1:8000 to view the frontend.
Click on the bell icon to see live notifications.

# 🔄 WebSocket Connection
A WebSocket connection is established at:

ws://127.0.0.1:8000/ws
New notifications will appear live without a page refresh.

###   API Endpoints
# ➕ Create Notification
# POST /notifications

## Body:
`{
  "user_id": 1,
  "message": "Your order has been shipped!"
}`

# 📥 Get All Notifications
# GET /notifications

Returns a list of all notifications.

# 📥 Get Notifications by User ID
GET /users/{user_id}/notifications

Replace {user_id} with the actual user ID.

### Documentation
Swagger UI is available at:
👉 http://127.0.0.1:8000/docs

### Troubleshooting
| Issue                                 | Solution                                                              |
|--------------------------------------|-----------------------------------------------------------------------|
| `DATABASE_URL` or DB connection error | Check `.env` file and make sure PostgreSQL is running                 |
| WebSocket not working                 | Ensure the URL matches `ws://127.0.0.1:8000/ws` and server is running |
| Notifications not displaying          | Inspect browser console for JS errors or check backend logs           |
