# Flowers API (Flask + MySQL)

## Project Overview
- This project is a RESTful API built using Flask and MySQL.
- It manages flower records and supports CRUD operations, search functionality, JWT authentication, and JSON/XML response formats.
- The project was developed as part of an academic requirement focused on API design, security, testing, and documentation.

## Project Features
- Create, Read, Update, Delete (CRUD) operations for flowers
- MySQL database integration
- Input validation and proper error handling
- JWT-based authentication for protected routes
- Search functionality using query parameters
- Supports JSON and XML response formats
- API endpoints tested using Postman

## Technologies Used
- Python 3
- Flask
- MySQL
- flask-mysqldb
- PyJWT
- dicttoxml
- pytest
- Postman

## Project Structure
- app.py – Main Flask application
- db.py – Database and JWT configuration
- test.py – Automated test cases
- requirements.txt – Project dependencies
- README.md – Project documentation

## Installation and Setup
- Clone the repository and navigate to the project folder
- Create and activate a virtual environment
- Install dependencies using `pip install -r requirements.txt`
- Create a MySQL database named `flowers`
- Create the `flower_list` table
- Configure database and JWT settings in `db.py`

## Running the Application
- Run the application using `python app.py`
- The API will be available at `http://127.0.0.1:5000`

## Authentication
- Login using the `/login` endpoint with admin credentials
- A JWT token is returned upon successful login
- Include the token in the `x-access-token` header for protected routes

## API Endpoints
- GET /health – Health check
- GET /flowers – Retrieve all flowers
- GET /flowers/<id> – Retrieve flower by ID
- POST /flowers – Create a new flower (JWT required)
- PUT /flowers/<id> – Update flower (JWT required)
- DELETE /flowers/<id> – Delete flower (JWT required)
- GET /flowers/search – Search flowers by name or color
- Optional format parameter: `?format=json` or `?format=xml`

## Testing
- All API features were manually tested using Postman
- Test cases include authentication, CRUD operations, search, and format validation
- Proper HTTP status codes were verified for success and error cases

## Notes
- JSON is the default response format
- XML output is available via query parameter
- JWT protects create, update, and delete operations
- Proper HTTP status codes are returned for all requests

## Author
- Luvna E. Arsi
- BSCS3 Block 1
