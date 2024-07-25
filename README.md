# AutoClient AI

AutoClient AI is a robust solution for web scraping and email marketing. It collects email addresses from websites, stores them in a PostgreSQL database, and facilitates the creation and management of email campaigns using SMTP.

## Table of Contents
1. [Setup Instructions](#setup-instructions)
2. [Folder Structure](#folder-structure)
3. [Environment Variables](#environment-variables)
4. [Dependencies](#dependencies)
5. [Database Schema](#database-schema)
6. [Application Overview](#application-overview)
7. [Frontend](#frontend)

## Setup Instructions
1. **Clone the Repository:**
    ```sh
    git clone https://github.com/your_repo/email-crawler.git
    cd email-crawler
    ```
2. **Configure Environment Variables:**
    
    Create a `.env` file in the root directory and include the following:
    
    ```
    PGDATABASE=your_db_name
    PGUSER=your_db_user
    PGPASSWORD=your_db_password
    PGHOST=your_db_host
    PGPORT=your_db_port
    SMTP_SERVER=your_smtp_server
    SMTP_PORT=your_smtp_port
    SMTP_USER=your_smtp_user
    SMTP_PASSWORD=your_smtp_password
    ```
3. **Install Required Dependencies:**
    
    ```sh
    pip install -r requirements.txt
    ```
4. **Launch the Application:**
    
    ```sh
    python app.py
    ```

## Folder Structure

email-crawler/
|-- static/
|   |-- main.js
|-- templates/
|   |-- index.html
|   |-- csv-table.html
|   |-- navbar.html
|   |-- campaign.html
|   |-- postgres-table.html
|   |-- view_campaign.html
|-- .env
|-- app.py
|-- requirements.txt
|-- README.md


## Environment Variables

The following environment variables are used in the application:

- **PGDATABASE**: PostgreSQL database name.
- **PGUSER**: PostgreSQL database user.
- **PGPASSWORD**: PostgreSQL database password.
- **PGHOST**: PostgreSQL database host.
- **PGPORT**: PostgreSQL database port.
- **SMTP_SERVER**: Your SMTP server address.
- **SMTP_PORT**: Your SMTP server port.
- **SMTP_USER**: Your SMTP username.
- **SMTP_PASSWORD**: Your SMTP password.

## Dependencies

Install dependencies using `pip`:
```sh
pip install -r requirements.txt