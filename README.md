# User Login API Project

## Summmary

this project is to develop a secure and efficient API system for user
authentication using email and One-Time Password (OTP). This system will enable
users to log in by providing their email address, receiving an OTP, and verifying the
OTP to gain access.

# Project Workflow Summary

## User sends email to /request-otp/

Email format and existence are validated.

OTP is generated, salted, hashed, and stored with a timestamp.

Sent to the user via mock email (printed to console).

## User submits OTP to /verify-otp/

Verifies OTP hash and checks expiration (30 sec).

On success, JWT access and refresh tokens are generated and returned.

## Security Measures

OTP is rate-limited (5/hour/email).

OTPs are hashed + salted.

Uses JWT for secure session management.

Docker support added for deployment.

## Mock OTP Delivery
Since this is a development/demo project, OTPs are printed to the console log as:
[MOCK EMAIL] OTP for test@example.com: 123456

# ADD Docker Setup Files Only in github Repo

## Dockerfile
FROM python:3.11.9          - Start with Python 3.11.9 as base
WORKDIR /api                -Set working directory to /api
COPY requirements.txt .     -Copy requirements file
RUN pip install ...        - Install Python packages
COPY . .                    -Copy your Django code
RUN adduser appuser         - Create secure user
USER appuser                -Switch to that user
EXPOSE 8000                 -Tell Docker app uses port 8000

## docker-compose.yaml
services:
  api:                      - Your Django container
    build: .                - Build using Dockerfile in current directory
    command: gunicorn...    - Override default command to run Gunicorn
    ports: "8000:8000"      - Map container port 8000 to host port 8000
    volumes: .:/app         - Mount current directory to /app (live code updates)
    depends_on: db          - Start database first
    
  db:                       - PostgreSQL database container
    image: postgres:15      - Use official PostgreSQL image
    environment: ...        - Set database credentials
    volumes: ...            - Persist database data

## Build and run
docker-compose up --build
This Django api is ready to work on any environment by docker containerzation.



 
