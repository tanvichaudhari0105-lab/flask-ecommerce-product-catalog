# E-Commerce Product Catalog

A web-based product catalog application built using Flask and MySQL, with REST APIs and Docker containerization.

## Technologies Used

- Python
- Flask
- MySQL
- REST API
- Docker
- Postman

## Features

- Add products
- View products
- Update products
- Delete products
- REST APIs for product management
- MySQL database integration
- Dockerized Flask application

## REST API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/products` | Get all products |
| GET | `/api/products/<id>` | Get a single product |
| POST | `/api/products` | Create a product |
| PUT | `/api/products/<id>` | Update a product |
| DELETE | `/api/products/<id>` | Delete a product |

## Docker

The Flask application is containerized using Docker and runs on port `5000`.

```bash
docker build -t flask-ecommerce .
docker run --rm -p 5000:5000 flask-ecommerce