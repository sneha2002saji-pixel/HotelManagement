"""
Module: models
Purpose: Defines data models for the Hotel Order Management Service.
Author: Developer Agent
Created: 2024-03-02
Notes: These models represent the core entities for room service orders, guests, and items.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Item(BaseModel):
    """
    Represents a single item available for room service.
    """
    item_id: str = Field(..., description="Unique identifier for the item")
    name: str = Field(..., description="Name of the item")
    description: Optional[str] = Field(None, description="Description of the item")
    price: float = Field(..., gt=0, description="Price of the item")
    stock_level: int = Field(..., ge=0, description="Current stock level of the item")

class Guest(BaseModel):
    """
    Represents a hotel guest.
    """
    guest_id: str = Field(..., description="Unique identifier for the guest (e.g., from PMS)")
    name: str = Field(..., description="Full name of the guest")
    room_number: str = Field(..., description="Room number of the guest")
    contact_information: Optional[str] = Field(None, description="Guest's contact information")

class OrderItem(BaseModel):
    """
    Represents an item within a room service order.
    """
    item_id: str = Field(..., description="ID of the ordered item")
    quantity: int = Field(..., gt=0, description="Quantity of the item ordered")
    price_at_order: float = Field(..., gt=0, description="Price of the item at the time of order")

class Order(BaseModel):
    """
    Represents a room service order.
    """
    order_id: str = Field(..., description="Unique identifier for the order")
    guest_id: str = Field(..., description="ID of the guest who placed the order")
    items: List[OrderItem] = Field(..., description="List of items in the order")
    delivery_instructions: Optional[str] = Field(None, description="Special delivery instructions")
    status: str = Field("Pending", description="Current status of the order (e.g., Pending, In Progress, Delivered, Cancelled)")
    total_cost: float = Field(..., ge=0, description="Total cost of the order")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the order was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the order was last updated")

class OrderCreate(BaseModel):
    """
    Data model for creating a new room service order.
    Does not include order_id, status, created_at, updated_at as these are system-generated.
    """
    guest_id: str = Field(..., description="ID of the guest who placed the order")
    items: List[OrderItem] = Field(..., description="List of items in the order")
    delivery_instructions: Optional[str] = Field(None, description="Special delivery instructions")

class OrderUpdate(BaseModel):
    """
    Data model for updating an existing room service order.
    All fields are optional for partial updates.
    """
    items: Optional[List[OrderItem]] = Field(None, description="List of items in the order")
    delivery_instructions: Optional[str] = Field(None, description="Special delivery instructions")
    status: Optional[str] = Field(None, description="Current status of the order (e.g., Pending, In Progress, Delivered, Cancelled)")
