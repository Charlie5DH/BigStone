import os
import pymongo
import json
from fastapi import FastAPI
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from typing import Optional, List
from models import Clients, Item, Transaction
from utils import convert_object_id

from database import get_clients_collection, get_items_collection, get_transactions_collection

app = FastAPI(title="Main Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients_collection = get_clients_collection()
items_collection = get_items_collection()
transactions_collection = get_transactions_collection()

CURRENT_WEIGHT = 0


@app.get("/test")
async def test():
    ''' API for testing the functionality of the server '''
    return {"message": "OK"}


@app.post("/api/create_client/", tags=["clients"])
async def create_client(client: Clients):
    ''' API for creating a new client:

    Attributes:
        _id (str): Unique ID of the client.
        name (str): Name of the client.
        email (EmailStr): Email of the client.
        cpf (str): CPF (Cadastro de Pessoas Físicas) of the client.
        rfid (str): RFID (Radio Frequency Identification) of the client.
        qrcode (str): QR code of the client (not implemented yet) (OPTIONAL)
        phone (Optional[str]): Phone number of the client.
        address (Optional[str]): Address of the client.
        cep (Optional[str]): CEP (Código de Endereçamento Postal) of the client.
        balance (float): Balance of the client.

    The generate_rfid validator is used to automatically generate a unique RFID tag using the uuid module if the rfid field is not provided.
    This ensures that a unique RFID is generated in real-time when needed.
    '''
    client_dict = client.__dict__

    # check if the client exists
    if clients_collection.find_one({"cpf": client_dict["cpf"]}) is not None:
        raise HTTPException(status_code=400, detail="Client already exists")

    result = clients_collection.insert_one(client_dict)

    created_client = clients_collection.find_one({"_id": result.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json.loads(json.dumps(created_client, default=convert_object_id)))


@app.get("/api/get_clients/", tags=["clients"])
async def get_clients():
    clients = list(clients_collection.find())
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(clients, default=convert_object_id)))


@app.get("/api/get_client/{client_id}", tags=["clients"])
async def get_client(client_id: str):
    client_data = clients_collection.find_one({"_id": ObjectId(client_id)})
    if client_data is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client_data


@app.put("/api/update_client/{client_id}", tags=["clients"])
async def update_client(client_id: str, client: dict):

    ''' API for updating a client:
    Attributes:
        client_id (str): Unique ID of the client.
        client (dict): Dictionary containing the fields to be updated.

    Example:
        {"name": "John Doe"}
    '''

    clients_collection.update_one(
        {"_id": ObjectId(client_id)}, {"$set": client})
    updated_client = clients_collection.find_one({"_id": ObjectId(client_id)})
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(updated_client, default=convert_object_id)))


@app.delete("/api/delete_client/{client_id}", tags=["clients"])
async def delete_client(client_id: str):
    clients_collection.delete_one({"_id": ObjectId(client_id)})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Client deleted successfully", "client_id": client_id})

##########################################################################################
# REMOTE
##########################################################################################


@app.post("/api/grant_access/{rfid}", tags=["rfid"])
async def grant_access(rfid: str):
    ''' API for granting access to a client using their RFID tag

    Attributes:
        rfid(str): RFID(Radio Frequency Identification) of the client.

    The rfid field is used to identify the client and grant access to them.
    '''
    client_data = clients_collection.find_one({"rfid": rfid})

    if client_data is None:
        raise HTTPException(
            status_code=404, detail="Client not found. It must be created first.")

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(client_data, default=convert_object_id)))


@app.post("/api/current_dish_weight/{weight}", tags=["weight"])
async def current_dish_weight(weight: float):
    ''' API for getting the current weight of the dish

    Attributes:
        weight(float): Current weight of the dish.

    The weight field is used to identify the current weight of the dish.
    '''
    global CURRENT_WEIGHT
    CURRENT_WEIGHT = weight

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(weight, default=convert_object_id)))


@app.get("/api/get_current_weight", tags=["weight"])
async def get_current_weight():
    ''' API for getting the current weight of the dish

    The weight field is used to identify the current weight of the dish.
    '''
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps({"weight": CURRENT_WEIGHT}, default=convert_object_id)))

##########################################################################################
# Items API
##########################################################################################


@app.get("/api/items/", tags=["items"])
async def get_items():
    '''
    API for getting all items in the database
    '''

    items = list(items_collection.find())
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(items, default=convert_object_id)))


@app.post("/api/items/", tags=["items"])
async def create_item(item: Item):
    '''
    API for creating a new item

    Attributes:
        name(str): Name of the item.
        description(str): Description of the item.
        price(float): Price of the item.
        quantity(int): Quantity of the item.
        barcode(str): Barcode of the item(OPTIONAL)
        image(str): Image of the item(OPTIONAL)
        category(str): Category of the item(OPTIONAL)
        tags(List[str]): Tags of the item(OPTIONAL)
    '''

    item_dict = item.__dict__
    result = items_collection.insert_one(item_dict)

    created_item = items_collection.find_one({"_id": result.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json.loads(json.dumps(created_item, default=convert_object_id)))


@app.get("/api/items/{item_id}", tags=["items"])
async def get_item(item_id: str):
    '''
    API for getting a specific item

    Attributes:
        item_id(str): Unique ID of the item.
    '''

    item_data = items_collection.find_one({"_id": ObjectId(item_id)})
    if item_data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(item_data, default=convert_object_id)))


@app.put("/api/items/{item_id}", tags=["items"], description="Update an item by its ID")
async def update_item(item_id: str, item: dict):
    '''
    API for updating an item

    Attributes:
        item_id(str): Unique ID of the item.
        item(dict): Dictionary containing the fields to be updated.
    Example:
        {"quantity": 2}
    '''

    items_collection.update_one(
        {"_id": ObjectId(item_id)}, {"$set": item})
    updated_item = items_collection.find_one({"_id": ObjectId(item_id)})

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(updated_item, default=convert_object_id)))


@app.put("/api/items/{item_id}/quantity", tags=["items"], description="Update the quantity of an item")
async def update_item_quantity(item_id: str, quantity: int):
    '''
    API for updating the quantity of an item

    Attributes:
        item_id(str): Unique ID of the item.
        quantity(int): New quantity of the item.

    '''

    items_collection.update_one(
        {"_id": ObjectId(item_id)}, {"$set": {"quantity": quantity}})
    updated_item = items_collection.find_one({"_id": ObjectId(item_id)})

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(updated_item, default=convert_object_id)))


@app.put("/api/items/{item_id}/subtract_quantity", tags=["items"], description="Subtract or add a quantity from an item")
async def subtract_item_quantity(item_id: str, quantity: int, subtract: bool = True):
    '''
    API for subtracting a quantity from an item

    Attributes:
        item_id(str): Unique ID of the item.
        quantity(int): Quantity to be subtracted from the item.
        subtract(bool): Whether to subtract or add the quantity(default: True)
    '''

    item_data = items_collection.find_one({"_id": ObjectId(item_id)})
    if item_data is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if subtract:
        new_quantity = item_data["quantity"] - quantity

        if new_quantity < 0:
            raise HTTPException(
                status_code=400, detail="Not enough items in stock, quantity cannot be negative")
    else:
        new_quantity = item_data["quantity"] + quantity

    items_collection.update_one(
        {"_id": ObjectId(item_id)}, {"$set": {"quantity": new_quantity}})
    updated_item = items_collection.find_one({"_id": ObjectId(item_id)})

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(updated_item, default=convert_object_id)))


@app.delete("/api/items/{item_id}", tags=["items"])
async def delete_item(item_id: str):
    '''
    API for deleting an item

    Attributes:
        item_id(str): Unique ID of the item.
    '''

    items_collection.delete_one({"_id": ObjectId(item_id)})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Item deleted successfully", "item_id": item_id})


@app.put("/api/items/", tags=["items"], description="Update many items at once")
async def update_many_items(ids: List[str], item: dict):
    '''
    API for updating many items at once

    Attributes:
        ids(List[str]): List of unique IDs of the items.
        item(dict): Dictionary containing the fields to be updated.
    '''

    items_collection.update_many(
        {"_id": {"$in": [ObjectId(id) for id in ids]}}, {"$set": item})
    updated_items = list(items_collection.find(
        {"_id": {"$in": [ObjectId(id) for id in ids]}}))

    if len(updated_items) == 0:
        raise HTTPException(status_code=404, detail="Items not found")

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(updated_items, default=convert_object_id)))


##########################################################################################
# Transaction API
##########################################################################################

@app.get("/api/transactions", tags=["transactions"])
async def get_transactions():
    '''
    API for getting all transactions
    '''

    transactions = list(transactions_collection.find())
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(transactions, default=convert_object_id)))


@app.get("/api/transactions/{transaction_id}", tags=["transactions"])
async def get_transaction(transaction_id: str):
    '''
    API for getting a specific transaction

    Attributes:
        transaction_id(str): Unique ID of the transaction.
    '''

    transaction_data = transactions_collection.find_one(
        {"_id": ObjectId(transaction_id)})
    if transaction_data is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(transaction_data, default=convert_object_id)))


@app.get("/api/transactions/{transaction_id}/items", tags=["transactions"])
async def get_transaction_items(transaction_id: str):
    '''
    API for getting the items of a specific transaction

    Attributes:
        transaction_id(str): Unique ID of the transaction.
    '''

    transaction_data = transactions_collection.find_one(
        {"_id": ObjectId(transaction_id)})
    if transaction_data is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(transaction_data["items"], default=convert_object_id)))


# get transactions by client_id or rfid
@app.get("/api/transactions/client", tags=["transactions"])
async def get_transactions_by_client(client_id: str = None, rfid: str = None):
    '''
    API for getting all transactions of a specific client

    Attributes:
        client_id(str): Unique ID of the client.
        rfid(str): RFID of the client.
    '''

    if client_id is not None:
        transactions = list(transactions_collection.find(
            {"client_id": client_id}))
    elif rfid is not None:
        transactions = list(
            transactions_collection.find({"client_rfid": rfid}))
    else:
        raise HTTPException(
            status_code=400, detail="Either client_id or rfid must be provided")

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(transactions, default=convert_object_id)))

# get transaction from a timestamp range


@app.get("/api/transactions/timestamp", tags=["transactions"])
async def get_transactions_by_timestamp(start_timestamp: str, end_timestamp: str, transaction_id: str = None):
    '''
    API for getting all transactions in a specific timestamp range

    Attributes:
        start_timestamp(str): Start timestamp of the range.
        end_timestamp(str): End timestamp of the range.
        transaction_id(str): Unique ID of the transaction.
    Example:
        http: // localhost: 8000/api/transactions/timestamp?start_timestamp = 2021-05-01T00: 00: 00 & end_timestamp = 2021-05-31T23: 59: 59
        start_timestamp and end_timestamp must be in ISO format: YYYY-MM-DDTHH: MM: SS
    '''

    start_timestamp = datetime.fromisoformat(start_timestamp)
    end_timestamp = datetime.fromisoformat(end_timestamp)

    if transaction_id is not None:
        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": start_timestamp}}, {
            "timestamp": {"$lte": end_timestamp}}, {"_id": ObjectId(transaction_id)}]}))
    else:
        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": start_timestamp}}, {
            "timestamp": {"$lte": end_timestamp}}]}))

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(transactions, default=convert_object_id)))


@app.post("/api/transactions", tags=["transactions"])
async def create_transaction(transaction: Transaction):
    '''
    Make a transaction.
    Transactions represents the flow of items from the warehouse to the client.

    The total and timestamp fields are automatically generated.
    The total is automatically subtracted from the client's balance.

    The current weight must is automatically updated when the transaction is made using the CURRENT_WEIGHT global

    Attributes:
        _id(str): Unique ID of the transaction.
        rfid(str): RFID(Radio Frequency Identification) of the client making the transaction.
        client_id(str): Unique ID of the client.
        items(List[dict]): List of items in the transaction and their prices.
        total(float): Total price of the transaction.
        timestamp(str): Timestamp when the transaction was created.
        kg_price (float): Price per kilogram of the dish.
        meal_price(float): Total price of the meal

    Example:
        {
            "rfid": "333907a32a974752869d7022183d6608",
            "items": [
                {
                "item_id": "64d2d745df6f0cfeed2cb223",
                "quantity": 2
                }
            ],
            "kg_price": 30
        }
    '''

    transaction_dict = transaction.__dict__

    # if only rfid is provided, get client_id from rfid and update the transaction_dict with the client_id
    # if both rfid and client_id are provided, check if they match
    # if only client_id is provided, update the transaction_dict with the rfid

    client = None

    if transaction_dict["rfid"] is not None:
        client = clients_collection.find_one(
            {"rfid": transaction_dict["rfid"]})
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        transaction_dict["client_id"] = str(client["_id"])
    elif transaction_dict["client_id"] is not None:
        client = clients_collection.find_one(
            {"_id": ObjectId(transaction_dict["client_id"])})
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        transaction_dict["rfid"] = client["rfid"]
    else:
        raise HTTPException(
            status_code=400, detail="Either rfid or client_id must be provided")

    # calculate total price of the transaction based on the items
    # check if items exist and if item is in stock
    transaction_dict["total"] = 0
    for item in transaction_dict["items"]:
        item_db = items_collection.find_one({"_id": ObjectId(item["item_id"])})
        if item_db is None:
            raise HTTPException(status_code=404, detail="Item not found")
        if item_db["quantity"] < item["quantity"]:
            # return how many items are in stock
            raise HTTPException(
                status_code=400, detail=f"Only {item_db['quantity']} items in stock")
        # add the name and the price of the item to the transaction
        item["name"] = item_db["name"]
        item["price"] = item_db["price"]
        transaction_dict["total"] += item_db["price"] * item["quantity"]

    # update the total price of the transaction based on the current weight of the dish
    transaction_dict["total"] += CURRENT_WEIGHT * transaction_dict["kg_price"]

    # add the weight of the dish to the transaction
    transaction_dict["weight"] = CURRENT_WEIGHT
    transaction_dict["meal_price"] = CURRENT_WEIGHT * \
        transaction_dict["kg_price"]

    # check if client has enough balance to make the transaction
    # if client["balance"] < transaction_dict["total"]:
    #     raise HTTPException(status_code=400, detail="Insufficient balance")

    # update item quantity
    for item in transaction_dict["items"]:
        items_collection.update_one(
            {"_id": ObjectId(item["item_id"])}, {"$inc": {"quantity": -item["quantity"]}})

    # create transaction
    result = transactions_collection.insert_one(transaction_dict)

    # update client balance
    clients_collection.update_one(
        {"_id": ObjectId(transaction_dict["client_id"])}, {"$inc": {"balance": -transaction_dict["total"]}})

    # return transaction created
    transaction_created = transactions_collection.find_one(
        {"_id": ObjectId(result.inserted_id)})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json.loads(json.dumps(transaction_created, default=convert_object_id)))


@app.delete("/api/transactions/{transaction_id}", tags=["transactions"])
async def delete_transaction(transaction_id: str):
    '''
    Delete a transaction.

    Attributes:
        transaction_id(str): Unique ID of the transaction.

    Example:
        http://localhost:8000/api/transactions/60a0b0b9e4b9a9b4a0f3b3a0
    '''

    # check if transaction exists
    transaction = transactions_collection.find_one(
        {"_id": ObjectId(transaction_id)})
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # update item quantity
    for item in transaction["items"]:
        items_collection.update_one(
            {"_id": ObjectId(item["item_id"])}, {"$inc": {"quantity": item["quantity"]}})

    # update client balance
    client = clients_collection.find_one(
        {"_id": ObjectId(transaction["client_id"])})
    clients_collection.update_one(
        {"_id": ObjectId(transaction["client_id"])}, {"$inc": {"balance": transaction["total"]}})

    # delete transaction
    transactions_collection.delete_one(
        {"_id": ObjectId(transaction_id)})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Transaction deleted successfully"})
