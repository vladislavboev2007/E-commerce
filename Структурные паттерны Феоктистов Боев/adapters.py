# adapters.py
from abc import ABC, abstractmethod
from typing import Dict, Any
import httpx
import json


class PaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount: float, order_data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class DeliveryService(ABC):
    @abstractmethod
    def schedule_delivery(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        pass


# Внешние сервисы с разными API
class StripePaymentAPI:
    def create_payment_intent(self, amount_cents: int, currency: str, metadata: dict) -> dict:
        # Эмуляция API Stripe
        return {
            "stripe_payment_id": f"pi_{id(self)}",
            "status": "succeeded",
            "amount_received": amount_cents
        }


class PayPalAPI:
    def make_payment(self, transaction_amount: float, item_list: list) -> dict:
        # Эмуляция API PayPal
        return {
            "paypal_transaction_id": f"PAY-{id(self)}",
            "state": "completed",
            "total_amount": transaction_amount
        }


class DHLDeliveryAPI:
    def create_shipment(self, recipient: dict, packages: list) -> dict:
        # Эмуляция API DHL
        return {
            "dhl_tracking_id": f"DHL{id(self)}",
            "status": "registered",
            "estimated_delivery": "2024-01-15"
        }


class FedExAPI:
    def request_delivery(self, ship_details: dict, commodities: list) -> dict:
        # Эмуляция API FedEx
        return {
            "fedex_tracking_number": f"FX{id(self)}",
            "service_type": "STANDARD",
            "commit_timestamp": "2024-01-16T12:00:00Z"
        }


# Адаптеры
class StripePaymentAdapter(PaymentService):
    def __init__(self):
        self.stripe = StripePaymentAPI()

    def process_payment(self, amount: float, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Адаптация данных под API Stripe
        amount_cents = int(amount * 100)
        metadata = {
            "order_id": order_data.get("order_id"),
            "user_id": order_data.get("user_id")
        }

        result = self.stripe.create_payment_intent(
            amount_cents=amount_cents,
            currency="usd",
            metadata=metadata
        )

        # Адаптация ответа под наш формат
        return {
            "payment_id": result["stripe_payment_id"],
            "status": result["status"],
            "amount": amount,
            "provider": "stripe"
        }


class PayPalPaymentAdapter(PaymentService):
    def __init__(self):
        self.paypal = PayPalAPI()

    def process_payment(self, amount: float, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Адаптация данных под API PayPal
        item_list = [
            {
                "name": f"Order {order_data.get('order_id')}",
                "price": amount,
                "quantity": 1
            }
        ]

        result = self.paypal.make_payment(amount, item_list)

        # Адаптация ответа под наш формат
        return {
            "payment_id": result["paypal_transaction_id"],
            "status": "completed" if result["state"] == "completed" else "failed",
            "amount": amount,
            "provider": "paypal"
        }


class DHLDeliveryAdapter(DeliveryService):
    def __init__(self):
        self.dhl = DHLDeliveryAPI()

    def schedule_delivery(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Адаптация данных под API DHL
        recipient = {
            "name": order_data.get("shipping_address", {}).get("name"),
            "address": order_data.get("shipping_address", {}).get("address")
        }

        packages = [{"weight": 1, "dimensions": "10x10x10"}]

        result = self.dhl.create_shipment(recipient, packages)

        # Адаптация ответа под наш формат
        return {
            "tracking_id": result["dhl_tracking_id"],
            "status": result["status"],
            "estimated_delivery": result["estimated_delivery"],
            "provider": "dhl"
        }


class FedExDeliveryAdapter(DeliveryService):
    def __init__(self):
        self.fedex = FedExAPI()

    def schedule_delivery(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Адаптация данных под API FedEx
        ship_details = {
            "recipient": order_data.get("shipping_address", {}).get("name"),
            "destination": order_data.get("shipping_address", {}).get("address")
        }

        commodities = [{"description": "E-commerce order"}]

        result = self.fedex.request_delivery(ship_details, commodities)

        # Адаптация ответа под наш формат
        return {
            "tracking_id": result["fedex_tracking_number"],
            "status": "scheduled",
            "estimated_delivery": result["commit_timestamp"],
            "provider": "fedex"
        }