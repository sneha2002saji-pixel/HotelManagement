"""
Module: order_service
Purpose: Provides business logic for managing room service orders.
Author: Developer Agent
Created: 2024-03-02
Notes: Currently uses in-memory storage. Future versions will integrate with PostgreSQL.
"""

from typing import Dict, List, Optional
from uuid import uuid4
from datetime import datetime

from src.models import Order, OrderCreate, OrderUpdate, Item, Guest, OrderItem

class OrderServiceError(Exception):
    """
    Custom exception for order service related errors.
    """
    pass

class OrderService:
    """
    Manages CRUD operations for room service orders.
    """

    def __init__(self):
        self.orders: Dict[str, Order] = {}
        self.items: Dict[str, Item] = {
            "item001": Item(item_id="item001", name="Club Sandwich", price=12.50, stock_level=50),
            "item002": Item(item_id="item002", name="Caesar Salad", price=10.00, stock_level=40),
            "item003": Item(item_id="item003", name="Orange Juice", price=4.00, stock_level=100),
            "item004": Item(item_id="item004", name="Mineral Water", price=3.00, stock_level=200),
        }
        self.guests: Dict[str, Guest] = {
            "guest001": Guest(guest_id="guest001", name="John Doe", room_number="101"),
            "guest002": Guest(guest_id="guest002", name="Jane Smith", room_number="205"),
        }

    def _calculate_total_cost(self, order_items: List[OrderItem]) -> float:
        """
        Calculates the total cost of an order based on its items.
        """
        total_cost = 0.0
        for order_item in order_items:
            item = self.items.get(order_item.item_id)
            if not item:
                raise OrderServiceError(f"Item with ID {order_item.item_id} not found.")
            if item.stock_level < order_item.quantity:
                raise OrderServiceError(f"Insufficient stock for item {item.name}. Available: {item.stock_level}, Requested: {order_item.quantity}")
            total_cost += order_item.quantity * item.price
        return total_cost

    def create_order(self, order_data: OrderCreate) -> Order:
        """
        Creates a new room service order.

        Args:
            order_data (OrderCreate): Data for the new order.

        Returns:
            Order: The newly created order.
        """
        if order_data.guest_id not in self.guests:
            raise OrderServiceError(f"Guest with ID {order_data.guest_id} not found.")

        order_id = str(uuid4())
        total_cost = self._calculate_total_cost(order_data.items)

        # Deduct from stock
        for order_item in order_data.items:
            self.items[order_item.item_id].stock_level -= order_item.quantity

        new_order = Order(
            order_id=order_id,
            guest_id=order_data.guest_id,
            items=order_data.items,
            delivery_instructions=order_data.delivery_instructions,
            total_cost=total_cost,
            status="Pending",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.orders[order_id] = new_order
        return new_order

    def get_order(self, order_id: str) -> Optional[Order]:
        """
        Retrieves a room service order by its ID.
        """
        return self.orders.get(order_id)

    def get_all_orders(self) -> List[Order]:
        """
        Retrieves all room service orders.
        """
        return list(self.orders.values())

    def update_order(self, order_id: str, update_data: OrderUpdate) -> Order:
        """
        Updates an existing room service order.
        """
        order = self.orders.get(order_id)
        if not order:
            raise OrderServiceError(f"Order with ID {order_id} not found.")

        if update_data.items:
            # Revert old stock and deduct new stock if items are updated
            for old_item in order.items:
                self.items[old_item.item_id].stock_level += old_item.quantity
            order.items = update_data.items
            order.total_cost = self._calculate_total_cost(order.items)
            for new_item in order.items:
                self.items[new_item.item_id].stock_level -= new_item.quantity

        if update_data.delivery_instructions is not None:
            order.delivery_instructions = update_data.delivery_instructions
        if update_data.status:
            order.status = update_data.status

        order.updated_at = datetime.now()
        self.orders[order_id] = order
        return order

    def cancel_order(self, order_id: str) -> Order:
        """
        Cancels a room service order and restores item stock.
        """
        order = self.orders.get(order_id)
        if not order:
            raise OrderServiceError(f"Order with ID {order_id} not found.")
        if order.status == "Cancelled":
            return order # Already cancelled

        order.status = "Cancelled"
        order.updated_at = datetime.now()

        # Restore stock
        for order_item in order.items:
            self.items[order_item.item_id].stock_level += order_item.quantity

        self.orders[order_id] = order
        return order

    def delete_order(self, order_id: str):
        """
        Deletes a room service order. (Note: In a real system, orders are usually cancelled, not deleted).
        """
        if order_id in self.orders:
            # In a real system, you might want to prevent deletion of non-cancelled orders
            # or ensure stock is restored if not already cancelled.
            del self.orders[order_id]
            return {"message": f"Order {order_id} deleted successfully."}
        raise OrderServiceError(f"Order with ID {order_id} not found.")
