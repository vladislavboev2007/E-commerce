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
class YooKassaAPI:
    def create_payment_intent(self, amount_cents: int, currency: str, metadata: dict) -> dict:
        # Эмуляция API ЮKassa
        return {
            "yookassa_payment_id": f"yk_{id(self)}",
            "status": "succeeded",
            "amount_received": amount_cents
        }


class SberAPI:
    def make_payment(self, transaction_amount: float, item_list: list) -> dict:
        # Эмуляция API Сбера
        return {
            "sber_transaction_id": f"sbr_{id(self)}",
            "state": "completed",
            "total_amount": transaction_amount
        }


class CDEKDeliveryAPI:
    def create_shipment(self, recipient: dict, packages: list) -> dict:
        # Эмуляция API СДЭК
        return {
            "cdek_tracking_id": f"CDEK{id(self)}",
            "status": "registered",
            "estimated_delivery": "2024-01-15",
            "delivery_price": 350.00
        }


class YandexMarketAPI:
    def request_delivery(self, ship_details: dict, commodities: list) -> dict:
        # Эмуляция API Яндекс.Маркет
        return {
            "yandex_tracking_number": f"YM{id(self)}",
            "service_type": "STANDARD",
            "commit_timestamp": "2024-01-16T12:00:00Z",
            "delivery_cost": 299.00
        }


# Адаптеры платежей
class YooKassaPaymentAdapter(PaymentService):
    def __init__(self):
        self.yookassa = YooKassaAPI()

    def process_payment(self, amount: float, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Адаптация данных под API ЮKassa
        amount_cents = int(amount * 100)
        metadata = {
            "order_id": order_data.get("order_id"),
            "user_id": order_data.get("user_id")
        }

        result = self.yookassa.create_payment_intent(
            amount_cents=amount_cents,
            currency="rub",
            metadata=metadata
        )

        # Адаптация ответа под наш формат
        return {
            "payment_id": result["yookassa_payment_id"],
            "status": result["status"],
            "amount": amount,
            "provider": "ЮKassa"
        }


class SberPaymentAdapter(PaymentService):
    def __init__(self):
        self.sber = SberAPI()

    def process_payment(self, amount: float, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Адаптация данных под API Сбера
        item_list = [
            {
                "name": f"Заказ №{order_data.get('order_id')}",
                "price": amount,
                "quantity": 1
            }
        ]

        result = self.sber.make_payment(amount, item_list)

        # Адаптация ответа под наш формат
        return {
            "payment_id": result["sber_transaction_id"],
            "status": "completed" if result["state"] == "completed" else "failed",
            "amount": amount,
            "provider": "Сбер"
        }


# Адаптеры доставки
class CDEKDeliveryAdapter(DeliveryService):
    def __init__(self):
        self.cdek = CDEKDeliveryAPI()

    def schedule_delivery(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Адаптация данных под API СДЭК
        recipient = {
            "name": order_data.get("shipping_address", {}).get("name"),
            "address": order_data.get("shipping_address", {}).get("address"),
            "phone": order_data.get("shipping_address", {}).get("phone", "+7XXXXXXXXXX")
        }

        packages = [{"weight": 1, "dimensions": "10x10x10", "id": 1}]

        result = self.cdek.create_shipment(recipient, packages)

        # Адаптация ответа под наш формат
        return {
            "tracking_id": result["cdek_tracking_id"],
            "status": result["status"],
            "estimated_delivery": result["estimated_delivery"],
            "delivery_price": result["delivery_price"],
            "provider": "СДЭК"
        }


class YandexMarketDeliveryAdapter(DeliveryService):
    def __init__(self):
        self.yandex = YandexMarketAPI()

    def schedule_delivery(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Адаптация данных под API Яндекс.Маркет
        ship_details = {
            "recipient": order_data.get("shipping_address", {}).get("name"),
            "destination": order_data.get("shipping_address", {}).get("address"),
            "phone": order_data.get("shipping_address", {}).get("phone", "+7XXXXXXXXXX")
        }

        commodities = [{"description": "Заказ из интернет-магазина", "amount": 1}]

        result = self.yandex.request_delivery(ship_details, commodities)

        # Адаптация ответа под наш формат
        return {
            "tracking_id": result["yandex_tracking_number"],
            "status": "scheduled",
            "estimated_delivery": result["commit_timestamp"],
            "delivery_price": result["delivery_cost"],
            "provider": "Яндекс.Маркет"
        }