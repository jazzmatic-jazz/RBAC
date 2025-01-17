## **PROJECT TITLE**
Role Based Access Control Management API

## **DESCRIPTION**
Backend system for a hypothetical organization that manages users, roles, and 
resources. The system should allow users with specific roles to perform actions on 
resources through a set of RESTful APIs. Implemented token-based authentication and 
enforce RBAC to control access to different endpoints.


## **Installation**

To install Project Title, follow these steps:
1. Clone the repository: **`git clone https://github.com/jazzmatic-jazz/RBAC.git`**
2. Navigate to the project directory: **`cd rbac_user`**
3. Install dependencies: **`pip install -r requirements.txt`**
4. Run Migrations: **`py manage.py makemigrations`**
5. Migrate: **`py manage.py migrate`**
6. Run the project: **`py manage.py runserver`**

## **API Endpoint**

1. Register user: **`api/auth/register`**
2. Login user: **`api/auth/login`**
3. Tasks Endpoint with HTTP VERBS (GET, PUT, POST, DELETE): **`api/users/`** **`api/resources/`**

## **POSTMAN COLLECTION**

[Link](https://bold-robot-237718.postman.co/workspace/Assessment~eb79b220-7ad9-4a19-ac44-e970b9543470/example/20228488-6117e58b-6f23-4326-a377-3e4a568e1674?action=share&creator=20228488&ctx=documentation&active-environment=20228488-e12cdb34-a84c-4651-893c-7559c89c4972)
