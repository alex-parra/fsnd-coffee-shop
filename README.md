# Coffee Shop Full Stack

2020-05-12 - Project for Udacity Fullstack Nanodegree

## Local setup

1. cd into `backend`
2. init virtual env: `python3 -m venv venv`
3. activate env: `source ./venv/bin/activate`
4. install dependencies: `python3 -m pip install -r requirements.txt`
5. start flask: `FLASK_APP=src/api.py flask run --reload`
6. cd into `frontend`
7. install dependencies: `yarn install`
8. start app: `yarn start`

## Endpoints

`GET /drinks`

- Returns all drinks in system
- Auth: Not required
- Returns `{ success: true, drinks: [] }`

`GET /drinks-detail`

- Returns all drinks in system with full details
- Auth: required + `get:drinks-detail` permission
- Returns `{ success: true, drinks: [] }`

`POST /drinks`

- Create a new drink
- Auth: required + `post:drinks` permission
- Returns 200 `{ success: true, drinks: [] }`
- Returns 422 if title is already in system

`PATCH /drinks/<id>`

- Update a drink
- Auth: required + `patch:drinks` permission
- Returns 200 `{ success: true, drinks: [] }`
- Returns 404 if `id` is not in system

`DELETE /drinks/<id>`

- Delete a drink
- Auth: required + `delete:drinks` permission
- Returns 200 `{ success: true, delete: id }`
- Returns 404 if `id` is not in system

## Auth Errors

`401` if Authorization header is missing or malformed  
`400` if 'permissions' are not in JWT payload  
`401` if a specific permission is not included in the users permissions. (this should be 403 but Postman tests for 401)

---

## Full Stack Nano - IAM Final Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

You have been called on to demonstrate your newly learned skills to create a full stack drink menu application. The application must:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## Tasks

There are `@TODO` comments throughout the project. We recommend tackling the sections in order. Start by reading the READMEs in:

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. You will need to complete the required endpoints, configure, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend for more details.](./frontend/README.md)
