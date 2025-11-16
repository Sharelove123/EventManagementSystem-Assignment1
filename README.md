## Note :- make sure to override the user model and then migrate changes🙂🙂.
 
 # EventManagementSystem-Assignment1

## Installation / Setup


1. Clone the repository:
   - git clone https://github.com/Sharelove123/EventManagementSystem-Assignment1.git

2. move to EventManagementSystem-Assignment1 folder:
   - cd EventManagementSystem-Assignment1

3. Create and activate a virtual environment:
   - Windows (PowerShell):
     - python -m venv .venv
     - \.venv\Scripts\Activate.ps1

4. Install dependencies from requirements.txt:
   - pip install -r requirements.txt

5. move to EventManagementSystem:
   - cd EventManagementSystem

6. Create Migrations:
   - python manage.py makemigrations

7. Apply Migrations:
   - python manage.py migrate

8. Django Server Command:
   - python manage.py runserver


## 🔗 API Endpoints

### 🧑‍💻 Authentication (`/api/auth/`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/auth/register/` | Register a new user |
| **POST** | `/api/auth/login/` | Log in and receive **JWT tokens** |
| **POST** | `/api/auth/logout/` | Log out current user |
| **POST** | `/api/auth/token/refresh/` | Refresh JWT access token |

**Example URLs:**
* `http://127.0.0.1:8000/api/auth/register/`
* `http://127.0.0.1:8000/api/auth/login/`

### 🎉 Events (`/api/core/events/`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/core/events/` | List all events |
| **POST** | `/api/core/events/` | Create a new event |
| **GET** | `/api/core/events/<event_id>/` | Retrieve a specific event |
| **PUT / PATCH** | `/api/core/events/<event_id>/` | Update an event |
| **DELETE** | `/api/core/events/<event_id>/` | Delete an event |

**Example URLs:**
* `http://127.0.0.1:8000/api/core/events/`
* `http://127.0.0.1:8000/api/core/events/1/`


### 📅 RSVP (`/api/core/events/<event_id>/rsvp/`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/core/events/<event_id>/rsvp/` | Create RSVP for an event |
| **PATCH** | `/api/core/events/<event_id>/rsvp/<rsvp_id>/` | Update RSVP status |

**Example URLs:**
* `http://127.0.0.1:8000/api/core/events/1/rsvp/`
* `http://127.0.0.1:8000/api/core/events/1/rsvp/3/`

### 📝 Reviews (`/api/core/events/<event_id>/reviews/`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/core/events/<event_id>/reviews/` | List reviews for an event |
| **POST** | `/api/core/events/<event_id>/reviews/` | Create a review |
| **GET** | `/api/core/events/<event_id>/reviews/<review_id>/` | Retrieve a specific review |
| **PUT / PATCH** | `/api/core/events/<event_id>/reviews/<review_id>/` | Update a review |
| **DELETE** | `/api/core/events/<event_id>/reviews/<review_id>/` | Delete a review |

**Example URLs:**
* `http://127.0.0.1:8000/api/core/events/1/reviews/`
* `http://127.0.0.1:8000/api/core/events/1/reviews/1/`



