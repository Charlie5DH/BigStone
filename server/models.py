import re
import uuid
from typing import Optional, List
from bson import ObjectId
from dataclasses import dataclass, asdict
from pydantic import BaseModel, Field, validator, constr
from pydantic import BaseModel, validator, root_validator
from datetime import datetime
from datetime import timedelta
import secrets


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Clients(BaseModel):
    """
    Clients Model:
    Represents client information.

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
    """
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., description="Name of the client",
                      example="John Doe")
    email: str = Field(..., description="Email of the client",
                       example="johndoe@example.com")
    cpf: constr(min_length=11, max_length=11) = Field(...,
                                                      description="CPF of the client", example="12345678901")
    rfid: str = Field(None, description="RFID of the client",
                      example="RFID123")
    qrcode: str = Field(None,
                        description="QR code of the client", example="QR123")
    phone: str = Field(
        "", description="Phone number of the client", example="555-123-4567")
    address: str = Field(
        "", description="Address of the client", example="123 Main St")
    cep: str = Field("", description="CEP of the client", example="12345-678")
    balance: float = Field(
        0.0, description="Balance of the client", example=0.0)
    created_at: str = Field(
        datetime.now().isoformat(), description="Timestamp when the client was created", example=datetime.now().isoformat())

    @validator("cpf")
    def validate_cpf_length(cls, v):
        if len(v) != 11:
            raise ValueError("CPF must have exactly 11 digits")
        return v

    @validator("email")
    def validate_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Email must be valid")
        return v

    @validator("rfid", pre=True, always=True)
    def generate_rfid(cls, v, values):
        if v is not None:
            return v  # RFID already provided
        else:
            # Generate a unique RFID using UUID
            generated_rfid = str(uuid.uuid4().hex)
            return generated_rfid

    # @validator("balance", pre=True, always=True)
    # def validate_balance(cls, v, values):
    #     if v is None:
    #         return 0.0
    #     if v < 0.0:
    #         raise ValueError("Balance must be greater than or equal to 0.0")
    #     else:
    #         return v

    @validator("qrcode", pre=True, always=True)
    def generate_qrcode(cls, v, values):
        if v is not None:
            return v
        else:
            generated_qrcode = str(uuid.uuid4().hex)
            return generated_qrcode

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "johndoe@example.com",
                "cpf": "12345678901",
                "phone": "(48)99-987-1234",
                "address": "Rua XXX, 123",
                "cep": "79311-571",
                "balance": 0.0
            }
        }


class Item(BaseModel):
    ''' Items Model:
    Represents item information.

    Attributes:
        _id (str): Unique ID of the item.
        name (str): Name of the item.
        description (str): Description of the item.
        price (float): Price of the item.
        quantity (int): Quantity of the item.
        created_at (str): Timestamp when the item was created.
        barcode (str): Barcode of the item (OPTIONAL)
        image (str): Image of the item (OPTIONAL)
        category (str): Category of the item (OPTIONAL)
        tags (List[str]): Tags of the item (OPTIONAL)
    '''

    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., description="Name of the item", example="Item 1")
    description: str = Field(..., description="Description of the item",
                             example="Item 1 description")
    price: float = Field(..., description="Price of the item", example=1.99)
    quantity: int = Field(..., description="Quantity of the item", example=1)
    image: str = Field(
        None, description="Image of the item", example="https://example.com/image.png")
    category: str = Field(
        "None", description="Category of the item", example="food")
    tags: List[str] = Field(
        [], description="Tags of the item", example=["food", "snack"])
    created_at: str = Field(datetime.now().isoformat(
    ), description="Timestamp when the item was created", example=datetime.now().isoformat())
    barcode: str = Field(
        None, description="Barcode of the item", example="123456789")

    @validator("price")
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("Price must be greater than 0")
        return v

    @validator("barcode", pre=True, always=True)
    def generate_barcode(cls, v, values):
        if v is not None:
            return v
        else:
            generated_barcode = str(uuid.uuid4().hex)
            return generated_barcode

    class Config:
        schema_extra = {
            "example": {
                "name": "Item 1",
                "description": "Item 1 description",
                "price": 1.99,
                "quantity": 1,
                "category": "food",
                "tags": ["food", "snack"],
                "image": "https://example.com/image.png"
            }
        }


class Transaction(BaseModel):
    ''' 
    Transaction Model:
    Represents transaction information.
    The transcations includes a list of items and products that can be weighted.

    Attributes:
        _id (str): Unique ID of the transaction.
        rfid (str): RFID (Radio Frequency Identification) of the client making the transaction.
        client_id (str): Unique ID of the client.
        items (List[dict]): List of items in the transaction and their prices.
        total (float): Total price of the transaction.
        timestamp (str): Timestamp when the transaction was created.
        current_weight (float): Current weight of the dish.
        kg_price (float): Price per kilogram of the dish.
    '''

    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    client_id: str = Field(
        "", description="Unique ID of the client", example="123456")
    rfid: str = Field(
        "", description="RFID of the client", example="RFID123")
    items: List[dict] = Field(..., description="List of items in the transaction and their prices", example=[{"item_id": "Item 1", "quantity": 1}, {
        "item_id": "Item 2", "quantity": 2}])
    total: float = Field(0, description="Total price of the transaction",
                         example=4.98)
    timestamp: str = Field(datetime.now().isoformat(
    ), description="Timestamp when the transaction was created", example=datetime.now().isoformat())

    # current_weight: float = Field(
    #     0, description="Current weight of the dish", example=0.0)
    kg_price: float = Field(
        0, description="Price per kilogram of the dish", example=0.0)
    meal_price: float = Field(
        0, description="Price of the meal", example=0.0)

    # validator for the total price, if the total price is not equal to the sum of the items prices, raise an error
    # @validator("total")
    # def validate_total(cls, v, values):
    #     if v < 0:
    #         raise ValueError("Total must be greater than 0")
    #     else:
    #         items = values.get("items")
    #         total = 0
    #         for item in items:
    #             total += item["price"] * item["quantity"]
    #         if v != total:
    #             raise ValueError(
    #                 "Total must be equal to the sum of the items prices")
    #         return v

    class Config:
        schema_extra = {
            "example": {
                "client_id": "123456",
                "rfid": "RFID123",
                "items": [{"item_id": "Item 1", "quantity": 1}, {"item_id": "Item 2", "quantity": 2}],
                # "current_weight": 0.0,
                "kg_price": 0.0
            }
        }


'''
Notes about the models:

Field(...): This indicates that the field is required and doesn't have a default value. It's a way of explicitly marking that the field must be provided when creating an instance of the Pydantic model.
Field(None): This indicates that the field is optional and can have a value of None. It's often used for fields that might not always have a value.
Field(default_value): This allows you to specify a default value for the field, which will be used if the field is not explicitly provided when creating an instance of the model.
Field(..., description="..."): You can provide a description for the field using the description parameter. This description can help provide context and documentation for the field.
Field(..., example="..."): The example parameter allows you to provide an example value for the field. This can be useful for documentation and testing purposes.
'''
