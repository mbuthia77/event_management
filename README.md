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
