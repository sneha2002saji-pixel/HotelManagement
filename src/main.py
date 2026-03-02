"""
Module: main
Purpose: FastAPI application for the Hotel Order Management Service.
Author: Developer Agent
Created: 2024-03-02
Notes: Defines API endpoints for managing room service orders.
"""

from fastapi import FastAPI, HTTPException, status
from typing import List

from src.models import Order, OrderCreate, OrderUpdate
from src.order_service import OrderService, OrderServiceError

app = FastAPI(title="Hotel Order Management Service", version="1.0.0")

order_service = OrderService()

@app.get("/health", status_code=status.HTTP_200_OK, summary="Health Check")
async def health_check():
    """
    Performs a health check on the service.
    Returns a simple status to indicate the service is running.
    """
    return {"status": "healthy", "message": "Hotel Order Management Service is operational"}

@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED, summary="Create a new room service order")
async def create_order(order_data: OrderCreate):
    """
    Creates a new room service order with the provided details.
    - **guest_id**: The ID of the guest placing the order.
    - **items**: A list of items and their quantities.
    - **delivery_instructions**: Optional special instructions for delivery.
    """
    try:
        order = order_service.create_order(order_data)
        return order
    except OrderServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/orders", response_model=List[Order], summary="Retrieve all room service orders")
async def get_all_orders():
    """
    Retrieves a list of all room service orders.
    """
    return order_service.get_all_orders()

@app.get("/orders/{order_id}", response_model=Order, summary="Retrieve a specific room service order by ID")
async def get_order(order_id: str):
    """
    Retrieves a single room service order by its unique ID.
    - **order_id**: The unique identifier of the order.
    """
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=Order, summary="Update an existing room service order")
async def update_order(order_id: str, update_data: OrderUpdate):
    """
    Updates an existing room service order identified by its ID.
    - **order_id**: The unique identifier of the order to update.
    - **update_data**: The fields to update (items, delivery_instructions, status).
    """
    try:
        order = order_service.update_order(order_id, update_data)
        return order
    except OrderServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/orders/{order_id}/cancel", response_model=Order, summary="Cancel a room service order")
async def cancel_order(order_id: str):
    """
    Cancels a room service order and restores the stock of its items.
    - **order_id**: The unique identifier of the order to cancel.
    """
    try:
        order = order_service.cancel_order(order_id)
        return order
    except OrderServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a room service order")
async def delete_order(order_id: str):
    """
    Deletes a room service order. Note: In a production system, orders are typically cancelled rather than deleted.
    - **order_id**: The unique identifier of the order to delete.
    """
    try:
        order_service.delete_order(order_id)
        return
    except OrderServiceError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
