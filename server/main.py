import os
import pymongo
import json
from fastapi import FastAPI, File, UploadFile
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, HTTPException, status, APIRouter, WebSocket
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from typing import Optional, List
from models import Clients, Item, Transaction
from utils import convert_object_id, get_init_and_end_timestamp_from_period
from typing import Annotated
from database import get_clients_collection, get_items_collection, get_transactions_collection, get_weights_collection, get_kg_price_collection

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
weights_collection = get_weights_collection()
kg_price_collection = get_kg_price_collection()

CURRENT_WEIGHT = 0
CURRENT_BARCODE = 0
KG_PRICE = 0

# intialize the server and get the last kg price in the database
# check if the kg_price collection is empty
if kg_price_collection.count_documents({}) == 0:
    # if it is empty, create a new kg_price document with the default value of 0
    kg_price_collection.insert_one(
        {"kg_price": 0, "timestamp": datetime.now().isoformat()})
    KG_PRICE = 0
else:
    # if it is not empty, get the last kg_price in the database
    last_kg_price = kg_price_collection.find_one(
        sort=[("timestamp", pymongo.DESCENDING)])
    KG_PRICE = last_kg_price["kg_price"]


# Store WebSocket clients in a set
websocket_clients = set()
websocket_clients_rfid = set()

# Function to send data to all WebSocket clients


async def send_data_to_clients(data):
    for client in websocket_clients:
        await client.send(data)

# WebSocket route to handle incoming WebSocket connections


@app.websocket("/ws/weight")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.add(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # You can process the received data here if needed.
            await send_data_to_clients(data)
    except Exception as e:
        print(f"WebSocket connection closed with error: {e}")
    finally:
        websocket_clients.remove(websocket)
        
@app.websocket("/ws/rfid_to_client")
async def websocket_endpoint_rfid(websocket: WebSocket):
    await websocket.accept()
    websocket_clients_rfid.add(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # You can process the received data here if needed.
            await send_data_to_clients(data)
    except Exception as e:
        print(f"WebSocket connection closed with error: {e}")
    finally:
        websocket_clients_rfid.remove(websocket)
        
        
@app.post("/api/registered_barcode/{barcode}", tags=["barcode"])
async def register_rfid_of_client(barcode: str):
    ''' API for setting the current RFID(barcode)
    
    Attributes:
        barcode(str): Current barcode of the client.
        
    The barcode field is used to identify the current barcode of the client.
    
    The saving and addition of the barcode will occur in the frontend. 
    This API receives the barcode from the Raspberry Pi, and locally saves it as the current registered user.
    Then, it sends the barcode to the frontend, which will add it to the list of registered users and to the current transaction,
    depending on the current state of the frontend.
    '''
    global CURRENT_BARCODE
    
    CURRENT_BARCODE = barcode
    
    print("CURRENT_BARCODE", CURRENT_BARCODE)
    
    # send the barcode to the frontend through the websocket
    for client in websocket_clients_rfid:
        message = {"type": "json", "message": "rfid", "value": barcode}
        await client.send_json(message)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(barcode, default=convert_object_id)))



@app.post("/api/current_dish_weight/{action}/{weight}/{timestamp}", tags=["weight"])
async def current_dish_weight(action: str, weight: float, timestamp: str):
    ''' API for setting the current weight of the dish

    Attributes:
        weight(float): Current weight of the dish.

    The weight field is used to identify the current weight of the dish.

    Save the current weight in the database for future reference
    '''
    # TODO: SEND CLIENT INFORMATION (RFID or ID) TO THE SERVER

    global CURRENT_WEIGHT

    if timestamp == "None" or timestamp == "":
        timestamp = datetime.now().isoformat()

    if action == "add":
        CURRENT_WEIGHT = weight

        for client in websocket_clients:
            message = {"type": "json",
                       "message": "new_weight",
                       "weight": weight,
                       "timestamp": timestamp}
            await client.send_json(message)

        # save the current weight in the database for future reference
        weights_collection.insert_one(
            {"weight": weight, "timestamp": timestamp})

        return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(weight, default=convert_object_id)))

    # cancel the current weight
    CURRENT_WEIGHT = 0

    for client in websocket_clients:
        message = {"type": "json", "message": "cancel",
                   "weight": 0, "timestamp": timestamp}
        await client.send_json(message)

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(weight, default=convert_object_id)))


@app.get("/test")
async def test():
    ''' API for testing the functionality of the server '''
    return {"message": "OK"}


@app.get("/api/get_image/{filename}")
async def get_image(filename: str):
    ''' API for getting an image from the assets folder

    Attributes:
        filename(str): Filename of the image.
    '''

    if not os.path.exists(f"app/assets/{filename}"):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(f"app/assets/{filename}")


@app.post("/api/upload_image")
async def create_upload_file(file: UploadFile | None = None):
    '''
    API for uploading an image to an item
    '''
    if not file:
        return {"message": "No upload file sent"}
    else:
        # save file in local storage (assets folder)
        with open((f"app/assets/{file.filename}"), "wb") as buffer:
            buffer.write(file.file.read())

        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Image uploaded successfully", "filename": file.filename})


@app.post("/api/create_clients", tags=["clients"])
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

    # check if the rfid is already in use
    if clients_collection.find_one({"rfid": client_dict["rfid"]}) is not None:
        raise HTTPException(status_code=400, detail="RFID already in use")

    result = clients_collection.insert_one(client_dict)

    created_client = clients_collection.find_one({"_id": result.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json.loads(json.dumps(created_client, default=convert_object_id)))


@app.get("/api/clients/", tags=["clients"])
async def get_clients():
    clients = list(clients_collection.find())
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(clients, default=convert_object_id)))


@app.get("/api/client/{client_id}", tags=["clients"])
async def get_client(client_id: str):
    client_data = clients_collection.find_one({"_id": ObjectId(client_id)})
    if client_data is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client_data

@app.get("/api/client/rfid/{rfid}", tags=["clients"])
async def get_client_by_rfid(rfid: str):
    client_data = clients_collection.find_one({"rfid": rfid})
    if client_data is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(client_data, default=convert_object_id)))  

@app.put("/api/client/{client_id}", tags=["clients"])
async def update_client(client_id: str, client: dict):

    ''' API for updating a client:
    Attributes:
        client_id (str): Unique ID of the client.
        client (dict): Dictionary containing the fields to be updated.

    Example:
        {"name": "John Doe"}
    '''

    # if balance is being updated, create a transaction of type "clear_debt" with the difference between the old and the new balance
    if "balance" in client:
        original_client = clients_collection.find_one(
            {"_id": ObjectId(client_id)})

        # create a transaction of type "clear_debt" with the difference between the old and the new balance
        transaction = {
            "client_name": original_client["name"],
            "client_email": original_client["email"],
            "rfid": original_client["rfid"],
            "client_id": original_client["_id"],
            "transaction_type": "clear_debt",
            "items": [],
            "total": float(client["balance"]) - float(original_client["balance"]),
            "timestamp": client["timestamp"],
            "kg_price": 0,
            "meal_price": 0,
            "weight": 0
        }
        transactions_collection.insert_one(transaction)

    # remove the timestamp from the client dict
    if "timestamp" in client:
        del client["timestamp"]

    clients_collection.update_one(
        {"_id": ObjectId(client_id)}, {"$set": client})
    updated_client = clients_collection.find_one({"_id": ObjectId(client_id)})
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(updated_client, default=convert_object_id)))


@app.delete("/api/client/{client_id}", tags=["clients"])
async def delete_client(client_id: str):
    clients_collection.delete_one({"_id": ObjectId(client_id)})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Client deleted successfully", "client_id": client_id})


@app.delete("/api/clients/{ids}", tags=["clients"])
async def delete_many_clients(ids: str):

    if type(ids) is list:
        pass
    elif type(ids) is str:
        if '[' in ids:
            ids = json.loads(ids)
        else:
            ids = [ids]
    else:
        raise TypeError('Field "ids" needs to be an id or a list of ids')

    clients_collection.delete_many(
        {"_id": {"$in": [ObjectId(id) for id in ids]}})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Clients deleted successfully", "client_ids": ids})


@app.put("/api/clients/clear_debt/{client_ids}", tags=["clients"])
async def clear_debt(client_ids: str):

    if type(client_ids) is list:
        pass
    elif type(client_ids) is str:
        if '[' in client_ids:
            client_ids = json.loads(client_ids)
        else:
            client_ids = [client_ids]
    else:
        raise TypeError(
            'Field "client_ids" needs to be an id or a list of ids')

    clients = list(clients_collection.find(
        {"_id": {"$in": [ObjectId(id) for id in client_ids]}}))

    clients_collection.update_many(
        {"_id": {"$in": [ObjectId(id) for id in client_ids]}}, {"$set": {"balance": 0}})
    updated_clients = list(clients_collection.find(
        {"_id": {"$in": [ObjectId(id) for id in client_ids]}}))

    # the timestamp of the transaction must be in the format 2023-09-04T22:17:57.835Z

    # create a transaction for each client to clear their debt
    for client in clients:
        transaction = {
            "client_name": client["name"],
            "client_email": client["email"],
            "rfid": client["rfid"],
            "client_id": client["_id"],
            "transaction_type": "clear_debt",
            "items": [],
            "total": float(client["balance"] * -1),
            "timestamp": datetime.now().isoformat(),
            "kg_price": 0,
            "meal_price": 0,
            "weight": 0
        }
        transactions_collection.insert_one(transaction)

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(updated_clients, default=convert_object_id)))


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


@app.get("/api/get_current_weight", tags=["weight"])
async def get_current_weight():
    ''' API for getting the current weight of the dish

    The weight field is used to identify the current weight of the dish.
    '''
    # # get the last weight in the database
    # last_weight = weights_collection.find_one(
    #     sort=[("timestamp", pymongo.DESCENDING)])
    # if last_weight is None:
    #     raise HTTPException(status_code=404, detail="Weight not found")

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps({"weight": CURRENT_WEIGHT}, default=convert_object_id)))


@app.post("/api/kg_price/{kg_price}", tags=["price"])
async def kg_price(kg_price: float):
    ''' API for getting the price per kilogram of the dish

    Attributes:
        kg_price(float): Price per kilogram of the dish.

    The kg_price field is used to identify the price per kilogram of the dish.
    '''
    global KG_PRICE
    KG_PRICE = kg_price

    # save the current kg_price in the database for future reference
    kg_price_collection.insert_one(
        {"kg_price": kg_price, "timestamp": datetime.now().isoformat()})

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(kg_price, default=convert_object_id)))


@app.get("/api/get_kg_price", tags=["price"])
async def get_kg_price():
    ''' API for getting the price per kilogram of the dish

    The kg_price field is used to identify the price per kilogram of the dish.
    '''
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps({"kg_price": KG_PRICE}, default=convert_object_id)))


##########################################################################################
# Items API
##########################################################################################


@app.get("/api/items/{sold_this_month}/{period}", tags=["items"])
async def get_items(sold_this_month: bool = False, period: int = 30):
    '''
    API for getting all items in the database

    Appends a field called "sold_this_month", "sold_this_week", "sold_today" to each item with the total 
    quantity of the item sold in the last month, week and day respectively.
    '''

    items = list(items_collection.find())

    transaction_type = "sell"
    if transaction_type == "all":
        filter_for_transaction_type = {}
    else:
        filter_for_transaction_type = {"transaction_type": transaction_type}

    # if sold_this_month is True, append the sold_this_month field to each item
    # we must take the transactions of the current month and sum the quantity of each item
    if sold_this_month:
        for item in items:
            # get the transactions of the current month
            start_timestamp = (
                datetime.now() - timedelta(days=period)).isoformat()
            end_timestamp = datetime.now().isoformat()
            transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": start_timestamp}}, {
                "timestamp": {"$lte": end_timestamp}}, filter_for_transaction_type]}))

            # get the transactions that contain the current item
            transactions_with_item = []
            for transaction in transactions:
                for item_in_transaction in transaction["items"]:
                    if item_in_transaction["item_id"] == str(item["_id"]):
                        transactions_with_item.append(transaction)

            # sum the quantity of the item in each transaction
            sold_this_month = 0
            sold_this_week = 0
            sold_today = 0
            for transaction in transactions_with_item:
                for item_in_transaction in transaction["items"]:
                    if item_in_transaction["item_id"] == str(item["_id"]):
                        sold_this_month += item_in_transaction["quantity"]

                        # check if the transaction was made in the last week
                        # Convert transaction timestamp to an offset-aware datetime object
                        transaction_timestamp = datetime.fromisoformat(
                            transaction["timestamp"]).replace(tzinfo=timezone.utc)

                        if datetime.now(timezone.utc) - timedelta(days=7) <= transaction_timestamp <= datetime.now(timezone.utc):
                            sold_this_week += item_in_transaction["quantity"]

                            # check if the transaction was made today
                            if datetime.now(timezone.utc) - timedelta(days=1) <= transaction_timestamp <= datetime.now(timezone.utc):
                                sold_today += item_in_transaction["quantity"]

            item["sold_this_month"] = sold_this_month
            item["sold_this_week"] = sold_this_week
            item["sold_today"] = sold_today

    # return the items sorted by name
    items = sorted(items, key=lambda item: item["name"])

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


@app.post("/api/items/many", tags=["items"])
async def create_many_items(items: List[Item]):
    '''
    API for creating many items at once

    Attributes:
        items(List[Item]): List of items to be created.
    '''

    items_dict = [item.__dict__ for item in items]
    result = items_collection.insert_many(items_dict)

    created_items = list(items_collection.find(
        {"_id": {"$in": result.inserted_ids}}))

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json.loads(json.dumps(created_items, default=convert_object_id)))


@app.post("/api/items/upload_image/{item_id}", tags=["images"])
async def create_upload_file(file: UploadFile | None = None, item_id: str = None):
    '''
    API for uploading an image to an item
    '''
    if not file:
        return {"message": "No upload file sent"}
    else:
        # save file in local storage (assets folder)
        with open((f"app/assets/{file.filename}"), "wb") as buffer:
            buffer.write(file.file.read())

        # update item image
        items_collection.update_one(
            {"_id": ObjectId(item_id)}, {"$set": {"image": file.filename}})
        updated_item = items_collection.find_one({"_id": ObjectId(item_id)})

        return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(updated_item, default=convert_object_id)))


@app.get("/api/items/image/{item_id}", tags=["images"])
async def get_item_image(item_id: str):
    '''
    API for getting the image of an item

    Attributes:
        item_id(str): Unique ID of the item.
    '''

    item_data = items_collection.find_one({"_id": ObjectId(item_id)})
    if item_data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if item_data["image"] is None:
        raise HTTPException(status_code=404, detail="Item image not found")
    return FileResponse(f"app/assets/{item_data['image']}")


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


@app.put("/api/items/{item_id}/quantity/{quantity}", tags=["items"], description="Update the quantity of an item")
async def update_item_quantity(item_id: str, quantity: int, user: dict):
    '''
    API for updating the quantity of an item

    The update must generate a transaction of type "stock" with the difference between the old and the new quantity

    Attributes:
        item_id(str): Unique ID of the item.
        quantity(int): New quantity of the item.
        user(dict): Dictionary containing the current user data.
    '''

    original_item = items_collection.find_one({"_id": ObjectId(item_id)})

    items_collection.update_one(
        {"_id": ObjectId(item_id)}, {"$set": {"quantity": quantity}})
    updated_item = items_collection.find_one({"_id": ObjectId(item_id)})

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # create a transaction of type "stock" with the difference between the old and the new quantity
    transaction = {
        "client_name": user["name"],
        "client_email": user["email"],
        "client_id": user["_id"],
        "transaction_type": "stock",
        "items": [
            {
                "item_id": item_id,
                "quantity": quantity - original_item["quantity"],
                "name": original_item["name"],
                "price": original_item["price"]
            }
        ],
        "total": original_item["price"] * (quantity - original_item["quantity"]),
        "timestamp": datetime.now().isoformat(),
        "kg_price": 0,
        "meal_price": 0,
        "weight": 0,
    }
    transactions_collection.insert_one(transaction)

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


@app.delete("/api/item/{item_id}", tags=["items"])
async def delete_item(item_id: str):
    '''
    API for deleting an item

    Attributes:
        item_id(str): Unique ID of the item.
    '''

    items_collection.delete_one({"_id": ObjectId(item_id)})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Item deleted successfully", "item_id": item_id})


@app.delete("/api/items/{ids}", tags=["items"])
async def delete_many_items(ids: str):

    if type(ids) is list:
        pass
    elif type(ids) is str:
        if '[' in ids:
            ids = json.loads(ids)
        else:
            ids = [ids]
    else:
        raise TypeError('Field "ids" needs to be an id or a list of ids')

    items_collection.delete_many(
        {"_id": {"$in": [ObjectId(id) for id in ids]}})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Items deleted successfully", "item_ids": ids})


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

@app.get("/api/transactions/{transaction_type}/{start_timestamp}/{end_timestamp}", tags=["transactions"])
async def get_transactions(transaction_type: str, start_timestamp: str = None, end_timestamp: str = None, limit: int = 0, skip: int = 0):
    '''
    API for getting all transactions

    Filter transactions by type: "sell", "stock", "clear_debt", "all"

    start_timestamp and end_timestamp must be in the format: YYYY-MM-DD and the timestamp in the database
    is in the format: YYYY-MM-DDTHH:MM:SS
    '''

    if transaction_type == "all":
        filter_for_transaction_type = {}
    else:
        filter_for_transaction_type = {"transaction_type": transaction_type}

    print("start_timestamp", start_timestamp)
    print("end_timestamp", end_timestamp)

    if start_timestamp is not None and end_timestamp is not None:

        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": start_timestamp}}, {
            "timestamp": {"$lte": end_timestamp}}, filter_for_transaction_type]}).skip(skip).limit(limit).sort("timestamp", pymongo.DESCENDING))
    else:
        transactions = list(transactions_collection.find(
            filter_for_transaction_type).skip(skip).limit(limit).sort("timestamp", pymongo.DESCENDING))

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(transactions, default=convert_object_id)))


@app.get("/api/transaction/{transaction_id}", tags=["transactions"])
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
@app.get("/api/transactions/client/{client_id}/period/{period}", tags=["transactions"])
async def get_transactions_by_client(client_id, period: str = "Hoje"):
    '''
    Get the transactions of a specific client in a specific period of time.

    Periods: "Hoje", "Ontem", "Últimos 7 dias", "Últimos 30 dias", "3 Mêses", "Selecione um período"

    Attributes:
        client_id(str): Unique ID of the client.
    '''
    transaction_type = "sell"

    if transaction_type == "all":
        filter_for_transaction_type = {}
    else:
        filter_for_transaction_type = {"transaction_type": transaction_type}

    start_timestamp, end_timestamp = get_init_and_end_timestamp_from_period(
        period)

    if client_id is not None:
        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": start_timestamp}}, {
            "timestamp": {"$lte": end_timestamp}}, {"client_id": client_id}, filter_for_transaction_type]}))
    else:
        raise HTTPException(
            status_code=400, detail="client_id must be provided")

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(transactions, default=convert_object_id)))


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

    transaction_type = "sell"

    if transaction_type == "all":
        filter_for_transaction_type = {}
    else:
        filter_for_transaction_type = {"transaction_type": transaction_type}

    if transaction_id is not None:
        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": start_timestamp}}, {
            "timestamp": {"$lte": end_timestamp}}, {"_id": ObjectId(transaction_id)}, filter_for_transaction_type]}))
    else:
        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": start_timestamp}}, {
            "timestamp": {"$lte": end_timestamp}}]}))

    # sort transactions by timestamp
    transactions = sorted(
        transactions, key=lambda transaction: transaction["timestamp"])

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
            "transaction_type": "sell",
            "items": [
                {
                "item_id": "64d2d745df6f0cfeed2cb223",
                "quantity": 2
                }
            ],
            "weight": 0,
            "kg_price": 30
        }
    '''

    transaction_dict = transaction.__dict__
    
    print(transaction_dict)

    # if only rfid is provided, get client_id from rfid and update the transaction_dict with the client_id
    # if both rfid and client_id are provided, check if they match
    # if only client_id is provided, update the transaction_dict with the rfid

    # if the kg_price is not provided, use the default KG_PRICE
    if transaction_dict["kg_price"] is None or transaction_dict["kg_price"] == "":
        transaction_dict["kg_price"] = KG_PRICE

    client = None

    if transaction_dict["rfid"] is not None:
        client = clients_collection.find_one(
            {"rfid": transaction_dict["rfid"]})
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        transaction_dict["client_id"] = str(client["_id"])
        transaction_dict["client_name"] = str(client["name"])
        transaction_dict["client_email"] = str(client["email"])
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
    if (transaction_dict["weight"] is None or transaction_dict["weight"] == "" or transaction_dict["weight"] != 0):
        transaction_dict["total"] += CURRENT_WEIGHT * transaction_dict["kg_price"]

    # add the weight of the dish to the transaction
    if (transaction_dict["weight"] is None or transaction_dict["weight"] == ""):
        transaction_dict["weight"] = CURRENT_WEIGHT
        transaction_dict["meal_price"] = CURRENT_WEIGHT * \
            transaction_dict["kg_price"]
    else:
        transaction_dict["meal_price"] = transaction_dict["weight"] * \
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
        {"_id": ObjectId(transaction_dict["client_id"])}, {"$inc": {"balance": -float(transaction_dict["total"])}})

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


@app.get("/api/transactions/summary/{period}", tags=["transactions"])
async def get_transactions_summary(period: str, start_timestamp: str = None, end_timestamp: str = None, limit: int = 0, skip: int = 0):
    '''
    Return a summary of transactions in a specific period of time.
    - Total sells
    - Total made
    - Total by meal
    - Total by item
    - Items sold
    - More selled items
    - Clients with more transactions
    - Clients that spent more money

    Periods: "Hoje", "Ontem", "Últimos 7 dias", "Últimos 30 dias", "3 Mêses", "Selecione um período"
    '''

    transaction_type = "sell"

    if transaction_type == "all":
        filter_for_transaction_type = {}
    else:
        filter_for_transaction_type = {"transaction_type": transaction_type}

    start_timestamp, end_timestamp = get_init_and_end_timestamp_from_period(
        period)

    transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": start_timestamp}}, {
        "timestamp": {"$lte": end_timestamp}}, filter_for_transaction_type]}).skip(skip).limit(limit))

    # total sells
    total_sells = len(transactions)

    # summary
    total_made = 0
    total_by_meal = 0
    total_by_item = 0
    items_sold = 0
    more_selled_items_in_period = []
    clients_with_more_transactions = []
    clients_that_spent_more_money = []

    for transaction in transactions:
        total_made += transaction["total"]
        total_by_meal += transaction["meal_price"]
        total_by_item += transaction["total"] - transaction["meal_price"]
        items_sold += len(transaction["items"])

        # more selled items of the period
        # create a dictionary with the item_id, the amount sold and the total made
        for item in transaction["items"]:
            item_in_period = next(
                (item_period for item_period in more_selled_items_in_period if item_period["item_id"] == item["item_id"]), None)
            if item_in_period is None:
                more_selled_items_in_period.append(
                    {"item_id": item["item_id"], "quantity": item["quantity"], "price": item["price"], "total": item["quantity"] * item["price"]})
            else:
                item_in_period["quantity"] += item["quantity"]
                item_in_period["total"] += item["quantity"] * item["price"]

        # clients with more transactions and how much they spent
        client_in_period = next(
            (client_period for client_period in clients_with_more_transactions if client_period["client_id"] == transaction["client_id"]), None)
        if client_in_period is None:
            clients_with_more_transactions.append(
                {"client_id": transaction["client_id"], "transactions": 1, "total": transaction["total"], "name": transaction["client_name"], "email": transaction["client_email"]})
        else:
            client_in_period["transactions"] += 1
            client_in_period["total"] += transaction["total"]

        # clients that spent more money
        client_in_period = next(
            (client_period for client_period in clients_that_spent_more_money if client_period["client_id"] == transaction["client_id"]), None)
        if client_in_period is None:
            clients_that_spent_more_money.append(
                {"client_id": transaction["client_id"], "total": transaction["total"], "name": transaction["client_name"], "email": transaction["client_email"]})
        else:
            client_in_period["total"] += transaction["total"]

    # sort the items by quantity
    more_selled_items_in_period.sort(
        key=lambda item: item["quantity"], reverse=True)
    # get the first 5 items
    more_selled_items = more_selled_items_in_period[:5]

    # sort the clients by transactions
    clients_with_more_transactions.sort(
        key=lambda client: client["transactions"], reverse=True)
    # get the first 5 clients
    clients_with_more_transactions = clients_with_more_transactions[:5]

    # sort the clients by total
    clients_that_spent_more_money.sort(
        key=lambda client: client["total"], reverse=True)
    # get the first 5 clients
    clients_that_spent_more_money = clients_that_spent_more_money[:5]

    # --------------------------------------------------------------------------------------------------------
    # create a daily summary of transactions which will be returned in the format
    # {"2021-05-01": {"total_sells": 1, "total_made": 10, "total_by_meal": 5, "total_by_item": 5, "items_sold": 1, clients_with_more_transactions": [], "clients_that_spent_more_money": []}}
    # the key is the date in isoformat
    # the value is a dictionary with the summary of the transactions of that day

    # get the first day of the period
    start_date = datetime.fromisoformat(start_timestamp).replace(
        hour=0, minute=0, second=0, microsecond=0)
    # get the last day of the period
    end_date = datetime.fromisoformat(end_timestamp).replace(
        hour=23, minute=59, second=59, microsecond=999999)
    # get the number of days in the period
    days = (end_date - start_date).days + 1
    # create a dictionary with the summary of the transactions of each day
    daily_summary = []

    for day in range(days):
        # get the date of the day
        date = start_date + timedelta(days=day)
        # get the transactions of the day
        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": date.isoformat()}}, {
            "timestamp": {"$lte": (date + timedelta(days=1)).isoformat()}}, filter_for_transaction_type]}))

        # summary
        total_made_daily = 0
        total_by_meal_daily = 0
        total_by_item_daily = 0
        items_sold_daily = 0
        clients_with_more_transactions_daily = []
        more_selled_items_in_period_daily = []

        for transaction in transactions:
            # more selled items of the day
            # create a dictionary with the item_id, the amount sold and the total made
            for item in transaction["items"]:
                item_in_period = next(
                    (item_period for item_period in more_selled_items_in_period_daily if item_period["item_id"] == item["item_id"]), None)
                if item_in_period is None:
                    more_selled_items_in_period_daily.append(
                        {"item_id": item["item_id"], "quantity": item["quantity"], "price": item["price"], "total": item["quantity"] * item["price"]})
                else:
                    item_in_period["quantity"] += item["quantity"]
                    item_in_period["total"] += item["quantity"] * item["price"]

            # clients with more transactions and how much they spent
            client_in_period = next(
                (client_period for client_period in clients_with_more_transactions_daily if client_period["client_id"] == transaction["client_id"]), None)
            if client_in_period is None:
                clients_with_more_transactions_daily.append(
                    {"client_id": transaction["client_id"], "transactions": 1, "total": transaction["total"], "name": transaction["client_name"], "email": transaction["client_email"]})
            else:
                client_in_period["transactions"] += 1
                client_in_period["total"] += transaction["total"]

            total_made_daily += transaction["total"]
            total_by_meal_daily += transaction["meal_price"]
            total_by_item_daily += transaction["total"] - \
                transaction["meal_price"]
            items_sold_daily += len(transaction["items"])

        # sort the clients by transactions
        clients_with_more_transactions_daily.sort(
            key=lambda client: client["transactions"], reverse=True)
        # get the first 5 clients
        clients_with_more_transactions_daily = clients_with_more_transactions_daily[:5]

        # add the summary of the day to the daily_summary dictionary
        daily_summary.append({
            "date": date.isoformat(),
            "total_sells": len(transactions),
            "total_made": total_made_daily,
            "total_by_meal": total_by_meal,
            "total_by_item": total_by_item_daily,
            "items_sold": items_sold_daily,
            "more_selled_items": more_selled_items_in_period_daily[:5] if len(more_selled_items_in_period_daily) > 5 else more_selled_items_in_period_daily,
            "clients_with_more_transactions_daily": clients_with_more_transactions_daily
        })

    # sort the daily summary by date in descending order
    daily_summary.sort(key=lambda day: day["date"], reverse=True)

    # -------------------------------------------------------------------------------------------------
    # create a daily summary for the transactions of type "stock"
    # get the first day of the period
    start_date = datetime.fromisoformat(start_timestamp).replace(
        hour=0, minute=0, second=0, microsecond=0)
    # get the last day of the period
    end_date = datetime.fromisoformat(end_timestamp).replace(
        hour=23, minute=59, second=59, microsecond=999999)
    # get the number of days in the period
    days = (end_date - start_date).days + 1
    # create a dictionary with the summary of the transactions of each day
    daily_stock_summary = []

    for day in range(days):
        # get the date of the day
        date = start_date + timedelta(days=day)
        # get the transactions of the day
        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": date.isoformat()}}, {
            "timestamp": {"$lte": (date + timedelta(days=1)).isoformat()}}, {"transaction_type": "stock"}]}))

        # summary
        total_made_daily_stock = 0
        items_sold_daily_stock = 0
        more_selled_items_in_period_daily_stock = []

        for transaction in transactions:
            # more selled items of the day
            # create a dictionary with the item_id, the amount sold and the total made
            for item in transaction["items"]:
                item_in_period = next(
                    (item_period for item_period in more_selled_items_in_period_daily_stock if item_period["item_id"] == item["item_id"]), None)
                if item_in_period is None:
                    more_selled_items_in_period_daily_stock.append(
                        {"item_id": item["item_id"], "quantity": item["quantity"], "price": item["price"], "total": item["quantity"] * item["price"]})
                else:
                    item_in_period["quantity"] += item["quantity"]
                    item_in_period["total"] += item["quantity"] * item["price"]

            total_made_daily_stock += transaction["total"]
            items_sold_daily_stock += len(transaction["items"])

        # add the summary of the day to the daily_summary dictionary
        daily_stock_summary.append({
            "date": date.isoformat(),
            "total_sells": len(transactions),
            "total_made": total_made_daily_stock,
            "items_sold": items_sold_daily_stock,
            "more_selled_items": more_selled_items_in_period_daily_stock,
        })

        # sort the daily summary by date in descending order
        daily_stock_summary.sort(key=lambda day: day["date"], reverse=True)

    # -------------------------------------------------------------------------------------------------
    # create a daily summary for the transactions of type "clear_debt"
    # get the first day of the period
    start_date = datetime.fromisoformat(start_timestamp).replace(
        hour=0, minute=0, second=0, microsecond=0)
    # get the last day of the period
    end_date = datetime.fromisoformat(end_timestamp).replace(
        hour=23, minute=59, second=59, microsecond=999999)
    # get the number of days in the period
    days = (end_date - start_date).days + 1
    # create a dictionary with the summary of the transactions of each day
    daily_clear_debt_summary = []

    for day in range(days):
        # get the date of the day
        date = start_date + timedelta(days=day)
        # get the transactions of the day
        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": date.isoformat()}}, {
            "timestamp": {"$lte": (date + timedelta(days=1)).isoformat()}}, {"transaction_type": "clear_debt"}]}))

        # summary
        total_made_daily_clear_debt = 0
        clients_with_transactions = []
        # clients with transactions contains the clients that made transactions in that day
        # in the format {"client_id": "123", "transactions": 1, "total": 10}

        for transaction in transactions:
            # get the clients that made transactions in that day and build the clients_with_transactions list
            client_in_period = next(
                (client_period for client_period in clients_with_transactions if client_period["client_id"] == transaction["client_id"]), None)
            if client_in_period is None:
                clients_with_transactions.append(
                    {"client_id": transaction["client_id"],
                     "transactions": 1,
                     "total": transaction["total"],
                     "name": transaction["client_name"],
                     "email": transaction["client_email"]})
            else:
                client_in_period["transactions"] += 1
                client_in_period["total"] += transaction["total"]

            total_made_daily_clear_debt += transaction["total"]

        # sort the clients by transactions
        clients_with_transactions.sort(
            key=lambda client: client["transactions"], reverse=True)

        # add the summary of the day to the daily_summary dictionary
        daily_clear_debt_summary.append({
            "date": date.isoformat(),
            "total_sells": len(transactions),
            "total_made": total_made_daily_clear_debt,
            "clients_with_transactions": clients_with_transactions
        })

    daily_clear_debt_summary.sort(key=lambda day: day["date"], reverse=True)

    # -------------------------------------------------------------------------------------------------

    summary = {
        "total_sells": total_sells,
        "total_made": total_made,
        "total_by_meal": total_by_meal,
        "total_by_item": total_by_item,
        "items_sold": items_sold,
        "more_selled_items": more_selled_items,
        "clients_with_more_transactions": clients_with_more_transactions,
        "clients_that_spent_more_money": clients_that_spent_more_money,
        "daily_summary": daily_summary,
        "daily_stock_summary": daily_stock_summary,
        "daily_clear_debt_summary": daily_clear_debt_summary
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(summary, default=convert_object_id)))


@app.get("/api/transactions/summary/{client_id}/period/{period}", tags=["transactions"])
async def get_transactions_summary_by_client(client_id, period: str = "Hoje"):
    '''
    Get the transactions summary of a specific client in a specific period of time.
    - Total sells
    - Total made
    - Total by meal
    - Total by item
    - Items sold
    - More selled items
    - Clients with more transactions
    - Clients that spent more money

    Periods: "Hoje", "Ontem", "Últimos 7 dias", "Últimos 30 dias", "3 Mêses", "Selecione um período"
    Attributes:
        client_id(str): Unique ID of the client.
    '''

    start_timestamp, end_timestamp = get_init_and_end_timestamp_from_period(
        period)

    if client_id is not None:
        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": start_timestamp}}, {
            "timestamp": {"$lte": end_timestamp}}, {"client_id": client_id}]}))
    else:
        raise HTTPException(
            status_code=400, detail="client_id must be provided")

    # total sells
    total_sells = len(transactions)
    # summary
    total_made = 0
    total_by_meal = 0
    total_by_item = 0
    items_sold = 0
    more_selled_items_in_period = []

    for transaction in transactions:
        total_made += transaction["total"]
        total_by_meal += transaction["meal_price"]
        total_by_item += transaction["total"] - transaction["meal_price"]
        items_sold += len(transaction["items"])

        # more selled items of the period
        # create a dictionary with the item_id, the amount sold and the total made
        for item in transaction["items"]:
            item_in_period = next(
                (item_period for item_period in more_selled_items_in_period if item_period["item_id"] == item["item_id"]), None)
            if item_in_period is None:
                more_selled_items_in_period.append(
                    {"item_id": item["item_id"], "quantity": item["quantity"], "price": item["price"], "total": item["quantity"] * item["price"]})
            else:
                item_in_period["quantity"] += item["quantity"]
                item_in_period["total"] += item["quantity"] * item["price"]

    # sort the items by quantity
    more_selled_items_in_period.sort(
        key=lambda item: item["quantity"], reverse=True)
    # get the first 5 items
    more_selled_items = more_selled_items_in_period[:5]

    # get the first day of the period
    start_date = datetime.fromisoformat(start_timestamp).replace(
        hour=0, minute=0, second=0, microsecond=0)
    # get the last day of the period
    end_date = datetime.fromisoformat(end_timestamp).replace(
        hour=23, minute=59, second=59, microsecond=999999)
    # get the number of days in the period
    days = (end_date - start_date).days + 1
    # create a dictionary with the summary of the transactions of each day
    daily_summary = []

    for day in range(days):
        # get the date of the day
        date = start_date + timedelta(days=day)
        # get the transactions of the day
        transactions = list(transactions_collection.find({"$and": [{"timestamp": {"$gte": date.isoformat()}}, {
            "timestamp": {"$lte": (date + timedelta(days=1)).isoformat()}}, {"client_id": client_id}]}))

        # summary
        total_made_daily = 0
        total_by_meal_daily = 0
        total_by_item_daily = 0
        items_sold_daily = 0
        more_selled_items_in_period_daily = []

        for transaction in transactions:
            # more selled items of the day
            # create a dictionary with the item_id, the amount sold and the total made
            for item in transaction["items"]:
                item_in_period = next(
                    (item_period for item_period in more_selled_items_in_period_daily if item_period["item_id"] == item["item_id"]), None)
                if item_in_period is None:
                    more_selled_items_in_period_daily.append(
                        {"item_id": item["item_id"], "quantity": item["quantity"], "price": item["price"], "total": item["quantity"] * item["price"]})
                else:
                    item_in_period["quantity"] += item["quantity"]
                    item_in_period["total"] += item["quantity"] * item["price"]

            total_made_daily += transaction["total"]
            total_by_meal_daily += transaction["meal_price"]
            total_by_item_daily += transaction["total"] - \
                transaction["meal_price"]
            items_sold_daily += len(transaction["items"])

        # add the summary of the day to the daily_summary dictionary
        daily_summary.append({
            "date": date.isoformat(),
            "total_sells": len(transactions),
            "total_made": total_made_daily,
            "total_by_meal": total_by_meal,
            "total_by_item": total_by_item_daily,
            "items_sold": items_sold_daily,
            "more_selled_items": more_selled_items_in_period_daily[:5] if len(more_selled_items_in_period_daily) > 5 else more_selled_items_in_period_daily
        })

    # sort the daily summary by date in descending order
    daily_summary.sort(key=lambda day: day["date"], reverse=True)

    summary = {
        "total_sells": total_sells,
        "total_made": total_made,
        "total_by_meal": total_by_meal,
        "total_by_item": total_by_item,
        "items_sold": items_sold,
        "more_selled_items": more_selled_items,
        "daily_summary": daily_summary
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(summary, default=convert_object_id)))
