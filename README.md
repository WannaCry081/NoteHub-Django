## NoteHubAPI - Django

NoteHubAPI is a simple Django-based API designed for managing notes within teams. It provides functionality for user authentication, team management, and note creation. The API supports both Swagger and Redoc for documentation purposes, ensuring ease of use and understanding for developers.

### Packages Used

- Django: Web framework for building the API.
- Django Rest Framework (DRF): Toolkit for building Web APIs in Django.
- Django Rest Framework SimpleJWT: Token-based authentication for DRF.
- drf-yasg: Library for generating Swagger/OpenAPI documentation for DRF APIs.

### Authentication Endpoints

- **POST** `/api/v1/auth/login/`: Endpoint for user login.
- **POST** `/api/v1/auth/register/`: Endpoint for user registration.
- **POST** `/api/v1/auth/blacklist/`: Endpoint to blacklist tokens.
- **POST** `/api/v1/auth/refresh/`: Endpoint to refresh tokens.

### User Endpoints

- **GET** `/api/v1/users/`: Retrieve all users.
- **PUT** `/api/v1/users/<pk>/`: Update user information.
- **PATCH** `/api/v1/users/<pk>/`: Update specific user information.
- **DELETE** `/api/v1/users/<pk>/`: Delete user.
- **GET** `/api/v1/users/<pk>/teams/`: Retrieve teams associated with a user.

### Team Endpoints

- **GET** `/api/v1/teams/`: Retrieve all teams.
- **GET** `/api/v1/teams/<pk>/`: Retrieve specific team.
- **POST** `/api/v1/teams/`: Create a new team.
- **POST** `/api/v1/teams/<pk>/join/`: Join a team.
- **PUT** `/api/v1/teams/<pk>/`: Update team information (permission required).
- **PATCH** `/api/v1/teams/<pk>/`: Update specific team information (permission required).
- **DELETE** `/api/v1/teams/<pk>/`: Delete team (permission required).
- **DELETE** `/api/v1/teams/<pk>/leave/`: Leave a team.

### Note Endpoints

- **GET** `/api/v1/notes/<pk>/`: Retrieve specific note.
- **PUT** `/api/v1/notes/<pk>/`: Update note.
- **POST** `/api/v1/notes/<pk>/`: Create new note.
- **PATCH** `/api/v1/notes/<pk>/`: Update specific note information.
- **DELETE** `/api/v1/notes/<pk>/`: Delete note.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/WannaCry081/NoteHubAPI-Django.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations:

    ```bash
    python manage.py migrate
    ```

4. Run the development server:

    ```bash
    python manage.py runserver
    ```

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.
