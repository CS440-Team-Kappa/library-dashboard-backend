# Library Dashboard Project Backend

Welcome to the Library Dashboard project backend, built with Django. This repository contains the backend component of our comprehensive library management system.

## Dependencies

The backend relies on the following libraries:

- **MySQLClient**: Enables communication and queries to be sent to the MySQL database.
- **CorsHeaders**: Allows JavaScript in a browser to make specific cross-origin requests.

## Setup Instructions

To set up the development environment, follow these steps:

1. **Install MySQLClient**:
    ```bash
    pip3 install mysqlclient
    ```
   This command installs the MySQLClient library, essential for communicating with the MySQL server.

2. **Install CorsHeaders**:
    ```bash
    pip3 install django-cors-headers
    ```
   This command installs the CorsHeaders library, which manages Cross-Origin Resource Sharing (CORS) in Django applications.

## How to Run

Once you've completed the setup steps, execute the following command from the project directory:

```bash
python3 backend/manage.py runserver
