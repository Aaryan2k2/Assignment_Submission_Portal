# Assignment Submission Portal

This project is a Django-based application for managing assignments, enabling users to submit, view, and manage their assignments efficiently.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Testing APIs in Postman](#testing-apis-in-postman)
- [License](#license)

## Features

- User authentication and registration
- Assignment submission and management
- View assignments
- Session-based authentication

## Technologies Used

- Django
- Django REST Framework
- PostgreSQL (or SQLite for development)
- Postman (for API testing)

## Setup

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- pip
- Django
- Virtualenv (optional but recommended)

### Clone the Repository

```bash
git clone https://github.com/Aaryan2k2/Assignment_Submission_Portal.git
cd Assignment_Submission_Portal
```
Running the Application
Start the development server with the following command:
```bash
python manage.py runserver
```
Your application will be accessible at http://127.0.0.1:8000/.


## API Endpoints
The application provides the following endpoints for users and admins:

## User Endpoints
## Register a new student
- Method: POST
- Endpoint: /student/register/
- Description: Registers a new student and returns a token for authentication.

## User login
- Method: POST
- Endpoint: /student/login/
- Description: Authenticates a student and returns a token for subsequent requests.
  
## Upload an assignment
- Method: POST
- Endpoint: /upload/
- Description: Allows a user to upload an assignment. Requires authentication token in the header.
  
## Fetch all admins
- Method: GET
- Endpoint: /admins/
- Description: Retrieves a list of all admins. Requires authentication token in the header.
- Admin Endpoints
  
## Register a new admin
- Method: POST
- Endpoint: /register/
- Description: Registers a new admin and returns a token for authentication.

## Admin login
- Method: POST
- Endpoint: /login/
- Description: Authenticates an admin and returns a token for subsequent requests.
 
## View assignments tagged to the admin
- Method: GET
- Endpoint: /assignments/
- Description: Allows an admin to view assignments assigned to them. Requires authentication token in the header.

## Accept an assignment
- Method: POST
- Endpoint: /assignments/<int:id>/accept/
- Description: Accepts an assignment by ID. Requires authentication token in the header.

## Reject an assignment
- Method: POST
- Endpoint: /assignments/<int:id>/reject/
- Description: Rejects an assignment by ID. Requires authentication token in the header.
