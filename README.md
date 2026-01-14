# SaaS Subscription Billing Platform

A complete cloud-native SaaS boilerplate with React, FastAPI, and Docker.

## Tech Stack
- **Frontend**: React, Vite, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy, Pydantic, APScheduler
- **Database**: MySQL 8.0
- **Infrastructure**: Docker Compose

## Prerequisites
- Docker & Docker Compose

## Quick Start

1. Start the application:
   ```bash
   docker-compose up --build
   ```

2. Access the services:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Features
- **User Authentication**: Register/Login with JWT.
- **Subscription Plans**: View and subscribe to monthly/yearly plans.
- **Background Billing**: Simulates recurring billing every minute (for demo).
- **Invoices**: View history and download mock PDF invoices.
- **Usage Tracking**: Placeholder for usage-based metrics.

## Development

### Backend
The backend is located in `./backend`. It uses `uvicorn` for development (hot-reload enabled in Docker).

### Frontend
The frontend is located in `./frontend`. It uses `vite` (hot-reload enabled in Docker).

## Configuration
Environment variables are defined in `docker-compose.yml`.
- `SECRET_KEY`: Change this for production.
- `DATABASE_URL`: Connection string for MySQL.
