# Project Title: Event Management API

## Description:
This API is designed to manage events, allowing users to create, update, and delete events. Additionally, it provides the functionality to view upcoming events. The project leverages Django ORM for database interactions and is deployed on Heroku or PythonAnywhere.

## Core Features and Functionality:
User Management:
User registration and authentication.
CRUD operations for user profiles.
Event Management:
Create, read, update, and delete events.
View details of individual events.
Upcoming Events:
Endpoint to fetch all upcoming events based on the current date.

## API Endpoints to Implement:
### User Endpoints:
`POST /api/users/`: Create a new user.
`GET /api/users/<id>/`: Retrieve a specific user.
`PUT /api/users/<id>/`: Update a specific user.
`DELETE /api/users/<id>/`: Delete a specific user.
### Event Endpoints:
`POST /api/events/`: Create a new event.
`GET /api/events/`: Retrieve all events.
`GET /api/events/<id>/`: Retrieve a specific event.
`PUT /api/events/<id>/`: Update a specific event.
`DELETE /api/events/<id>/`: Delete a specific event. 
### Upcoming Events Endpoint:
`GET /api/events/upcoming/`: Retrieve all upcoming events.

## Tools and Libraries:
- Django: For building the web application.
- Django REST Framework: For creating the API.
- MySQL: As the database.
- mysqlclient: To connect Django with MySQL.
- Gunicorn: For serving the Django application on Heroku.
- Heroku: For deployment.
- Django ORM: For database interactions.


# Event Management API

## Setup Instructions

### Prerequisites
- Python 3.x
- pip (Python package installer)
- virtualenv

### Setup

1. Create a virtual environment:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

2. Install dependencies:
    ```sh
    pip install django
    ```

3. Start the Django project:
    ```sh
    django-admin startproject event_management
    cd event_management
    ```

4. Create the initial app:
    ```sh
    python manage.py startapp events
    ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```

### Additional Commands

- To create a superuser for the admin site:
    ```sh
    python manage.py createsuperuser
    ```

## Contributing

1. Fork the repository.
2. Create your feature branch:
    ```sh
    git checkout -b my-new-feature
    ```
3. Commit your changes:
    ```sh
    git commit -am 'Add some feature'
    ```
4. Push to the branch:
    ```sh
    git push origin my-new-feature
    ```
5. Create a new Pull Request.

## License
This project is licensed under the MIT License.
