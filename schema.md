# TO DO LIST APP

- LEARNING: 
    1. User Authentication
    2. CRUD Operations

## SCHEMA

- RESTful API is required to have the following endpoints: 
    1. User registration to create a new user
    2. Login endpoint to authenticate the user and generate a token
    3. CRUD operations for managing the to-do list
    4. Implement user authentication to allow only authorized users to access the to-do list
    5. Implement error handling and security measures
    6. Use a database to store the user and to-do list data 
    7. Implement proper data validation
    8. Implement pagination and filtering for the to-do list

- USER REGISTRATION:
    1. user should be able to sign up / create a new account

    2. Request format:
    POST /register
    {
    "name": "John Doe",
    "email": "john@doe.com",
    "password": "password"
    } 

    3. Email should be validated
        (i) it should be a valid email (using regex)
        (ii) it should be unique => no previous entry of this email should exist in the database - if 
        there already exists sent email in the database, post request should fail

    4. password should be hashed before storing in database (best hashing algorithm should be searched)

    5. If the registration is successful, create a new account, add it to the database, and respond with
    a authentication token => this token can be used by user for subsequent tasks which will require authentication.

    6. If the email already exists in the DB, respond with a 409 (Conflict) Error Code.


- USER LOGIN:
    1.  FORMAT:
    POST /login
    {
    "email": "john@doe.com",
    "password": "password"
    }

    2. validate the account, and respond with the authentication token.

    3. if login fails, respond with a 401 (Unauthorized) Error Code.
    {
        "message": "Unauthorized"
    }

**Client requests must contain *Authorization* header for CRUD operations.**
**Authorization header is simple the *Authentication Token* previously provided at the time of login/signup**

- CREATE A TO-DO ITEM:
    1. FORMAT:
    POST /todos
    {
    "title": "Buy groceries",
    "description": "Buy milk, eggs, and bread"
    }

    2. If missing **Authorization** header, respond with a 401 (Unauthorized) Error Code.
    {
        "message": "Unauthorized"
    }

    3. Upon, successful creation of to-do item, respond with the details of the created item
    {
    "id": 1,
    "title": "Buy groceries",
    "description": "Buy milk, eggs, and bread"
    }


- UPDATE TO-DO ITEM:
    1. FORMAT:
    PUT /todos/1
    {
    "title": "Buy groceries",
    "description": "Buy milk, eggs, bread, and cheese"
    }

    2. If missign authorization header, respond with 401 Error Code

    3. API must check the whether the user is authorized to the operation, which is that client
    must be the creator of the to-do item

    4. If client is not authorized for this operation, respond with a 403(Forbidden) Error Code
    {
        "message": "Forbidden"
    }

    5. Upon successful updation of to-do item, respond with the updated to-do item
    {
    "id": 1,
    "title": "Buy groceries",
    "description": "Buy milk, eggs, bread, and cheese"
    }


- DELETE A TO-DO ITEM:
    1. FORMAT:
    DELETE /todos/1

    2. User must be authorized and authenticated to do carry out the operation

    3. if unauthenticated, respond with 401 status

    4. if unauthorized, respond with 409 status

    5. upon successful deletion, respond with 204(No content: deletion is successful but there is no response data) status code

- GET A TO-DO ITEM:
    1. FORMAT:
    GET /todos?page=1&limit=10
 
    2. RESPONSE FORMAT:
    {
    "data": [
        {
        "id": 1,
        "title": "Buy groceries",
        "description": "Buy milk, eggs, bread"
        },
        {
        "id": 2,
        "title": "Pay bills",
        "description": "Pay electricity and water bills"
        }
    ],
    "page": 1,
    "limit": 10,
    "total": 2
    }

    3. Response should be paginated


### HOW TO USE THE TOKEN FOR AUTHENTICATING THE USER
### WHAT KIND OF AUTHENTICATION TOKEN TO USE (JWT OR OTHER)
### DATABASE SCHEMA
### HOW TO CHECK WHETHER THE CLIENT IS THE CREATOR OF TO-DO ITEM
