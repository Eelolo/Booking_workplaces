# Booking_workplaces
An application that provides booking of workplaces in offices.

### Create Python virtual environment 
```
python3 -m venv venv
```
### Activate it
Run from `${project_root}:
```
. venv/bin/activate
```
### To deactivate run:
```
deactivate
```
### Install dependencies
Run from `${project_root}:
```
pip install -r requirements.txt
```

### Fill configuration in .env:
```
cp .env-example .env
```
### Make database migration:
Run from `${project_root}: 
```
python manage.py migrate
```
if required:
```
python manage.py makemigration
```
and again:
```
python manage.py migrate
```
# Usage:

## To create superuser:
Run from `${project_root}:
```
python manage.py createsuperuser
```
## Run tests:
Run from `${project_root}:
```
python manage.py test
```
## Run server:
Run from `${project_root}:
```
python manage.py runserver
```
# Endpoints
## /users/
#### Methods: "POST", "GET". 
Send "GET" request to get a list of users, if you are logged in.
Send "POST" request to create new user:
```
{
  "username": "some_username",
  "password": "some_password"
}
```
## /token/login/ 
#### Methods: "POST".
Use to get authentication token. Use a token for all endpoints that require authorization.
For this you need to send a token in the request headers:
```
"Authorization": "Token 4f9437a69fb8b05084fc9b46854e14acfd79093f"
```

## /users/me/
#### Methods: "GET", "PUT", "PATCH".

GET : returns your account information
PUT : takes field to update
Example:
```
{"email": "newemail@gmail.com"}
```
PATCH : takes all ruquired fields to update.
Example:
```
{
  "email": "newemail@gmail.com",
  "username": "neweusername"
}
```
Some endpoints that Djoser library provide:
```
/users/set_password/
/users/set_username/ 
/token/logout/
```
More details: https://djoser.readthedocs.io/en/latest/index.html

## office/create/
#### Methods: "POST".
Using for create new office. Allowed only admin users.
Example:
```
{
    "workplaces": 5
}
```
## offices/
#### Methods: "GET".
Returns a list of all offices

## office/edit/<int:pk>/
#### Methods: "GET", "PATCH", "DELETE".
Using for edit office. Allowed only admin users.
{
    "workplaces": 10
}

## workplace/create/
#### Methods: "POST".
Using for create new workplace. Allowed only admin users.
Example:
```
{
    "office": 2,
    "price": 1000
}
```

## workplaces/
#### Methods: "GET".
Returns a list of all workplaces.

## workplaces/<date_from>/<date_to>/
#### Methods: "GET".
Returns a list of all workplaces available for booking within a specified time frame.
Accepts dates in iso format:
```
workplaces/2021-01-11/2021-01-15/
```

## workplace/edit/<int:pk>/
#### Methods: "GET", "PATCH", "DELETE".
Using for edit workplace. Allowed only admin users.
Example:
```
{
    "price": 1500,
}
```

## reservation/create/
#### Methods: "POST".
Using for create new reservation. You cannot specify the start of the booking later than one month from the current date. 
The duration of the booking should not exceed 2 weeks. Does not allowed intersection by dates.
Example:
```
{
    "office": 1,
    "initial_day": "2021-01-21",
    "reservation_ends": "2021-01-22",
    "user": "SomeUser",
    "workplace": 1
}
```

## reservations/
#### Methods: "GET".
Returns a list of all reservations.

## reservations/<int:pk>/
#### Methods: "GET".
Returns a list of bookings for the selected workplaces.

## reservation/edit/<int:pk>/
#### Methods: "GET", "PATCH", "DELETE".
Using for edit reservation. The user can only change or delete their own booking. 
When editing, all validations are performed as when creating. Allowed only admin users.
GET : returns selected reservation
PATCH : takes fields to change
Example:
```
{
    "reservation_ends": "2021-01-22",
    "user": "SomeUser",
    "workplace": 3
}
```
DELETE : deletes the selected booking
