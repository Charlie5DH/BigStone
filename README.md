# BIG STONE PROJECT

<img src="resources\flow_bg_white.svg" alt="flow" style="zoom: 30%;" />

## 1. Introduction

## 2. Installation

1. Clone the repository.
2. Run `docker-compose up -d --build` to build the containers.
3. Go to `localhost:8003/docs` for API documentation

## 3. Data

Go to Server folder and open the `models.py` file to see the models and their attributes.

The `main.py` file contains the API endpoints.

### Clients Model:

The Clients Model represents client information for a business or service. It includes attributes such as `_id`, `name`, `email`, `cpf` (Cadastro de Pessoas Físicas), `rfid` (Radio Frequency Identification), `qrcode`, `phone`, `address`, `cep` (Código de Endereçamento Postal), and balance. The model is designed to manage and track client details, generate unique RFIDs and QR codes, and ensure valid email and CPF formats. The provided validators ensure data integrity and facilitate automatic generation of unique identifiers. The model is intended for use cases where client information and balances need to be managed seamlessly.

### Items Model:

The Items Model represents information about items available in a store or inventory. It includes attributes such as `_id`, `name`, `description`, `price`, `quantity`, `image`, `category`, `tags`, and `barcode`. The validators ensure that the price is valid and provide automatic barcode generation if not provided. This model is suitable for managing and organizing inventory items, enabling efficient tracking and retrieval.

### Transaction Model:

The Transaction Model captures information about transactions involving clients and items. It includes attributes such as `_id`, `client_id`, `rfid`, `items`, `total`, `timestamp`, `kg_price`, and `meal_price`. This model is tailored for `tracking purchases`, particularly in contexts where items can be weighed and priced by kilogram. The model's items field allows for listing multiple items in a transaction, and the total field calculates the overall transaction price. This model is well-suited for scenarios where clients make purchases, and the transaction involves both individual items and weighted products, providing a comprehensive overview of the transaction details.

<img src="resources\APIs.png" alt="logo" style="zoom: 100%;" />

## 4. Folder structure

Folder structure for the project:

```bash
resources
    ├── flow_bg_white.svg # Flow diagram
    ├── flow_bg.svg # Flow diagram
    ├── flow.svg # Flow diagram
    ├── logo.svg # Logo
server
    ├── Dockerfile # Dockerfile for the FastAPI server
    ├── README.md
    ├── main.py # Main file for the FastAPI server
    ├── models.py # Contains the models for the database
    ├── requirements.txt # Requirements for the FastAPI server
    ├── utils.py # Contains the functions for the FastAPI server
    └── database # connection to the database
data # Contains the data for the database (ensures persistence)
    ├── main_db
        ├── journal
        ...
.env # Environment variables
.dockerignore # Dockerignore file
.gitignore # Gitignore file
docker-compose.yml # Docker compose file
README.md # Readme file
```

## 5. Technologies

- Python 3.12
- Docker
- MongoDB
- FastAPI

- NextJS
- TailwindCSS
