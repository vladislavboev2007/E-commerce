# composite.py
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List


class CatalogComponent(ABC):
    @abstractmethod
    def get_price(self) -> Decimal:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        pass


class ProductLeaf(CatalogComponent):
    def __init__(self, product_id: int, name: str, price: Decimal, description: str):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description

    def get_price(self) -> Decimal:
        return self.price

    def get_description(self) -> str:
        return self.description

    def display(self, indent: int = 0) -> str:
        return "  " * indent + f"Товар: {self.name} - {self.price}₽"


class ProductComposite(CatalogComponent):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.children: List[CatalogComponent] = []

    def add(self, component: CatalogComponent):
        self.children.append(component)

    def remove(self, component: CatalogComponent):
        self.children.remove(component)

    def get_price(self) -> Decimal:
        total = Decimal('0.00')
        for child in self.children:
            total += child.get_price()
        return total

    def get_description(self) -> str:
        return self.description

    def display(self, indent: int = 0) -> str:
        result = "  " * indent + f"Набор: {self.name} (Всего: {self.get_price()}₽)\n"
        for child in self.children:
            result += child.display(indent + 1) + "\n"
        return result

    def get_products_list(self) -> List[dict]:
        """Возвращает список товаров в наборе для корзины"""
        products = []
        for child in self.children:
            if isinstance(child, ProductLeaf):
                products.append({
                    'id': child.product_id,
                    'name': child.name,
                    'price': float(child.price)
                })
        return products


class CatalogManager:
    def __init__(self):
        self.bundles = {}

    def create_computer_bundle(self) -> ProductComposite:
        bundle = ProductComposite("Игровой компьютер", "Полный игровой комплект")

        bundle.add(ProductLeaf(2, "Ноутбук ASUS ROG", Decimal('124999.99'), "Игровой ноутбук ASUS ROG Strix"))
        bundle.add(ProductLeaf(3, "Наушники AirPods Pro", Decimal('18999.99'), "Беспроводные наушники с шумоподавлением"))
        bundle.add(ProductLeaf(5, "Умные часы Galaxy Watch", Decimal('24999.99'), "Samsung Galaxy Watch 6"))

        self.bundles["gaming_computer"] = bundle
        return bundle

    def create_office_bundle(self) -> ProductComposite:
        bundle = ProductComposite("Офисный набор", "Всё для работы в офисе")

        bundle.add(ProductLeaf(8, "Пылесос Dyson", Decimal('29999.99'), "Беспроводной пылесос Dyson V15"))
        bundle.add(ProductLeaf(9, "Кофемашина DeLonghi", Decimal('45999.99'), "Автоматическая кофемашина"))
        bundle.add(ProductLeaf(11, "Коврик для йоги", Decimal('1299.99'), "Коврик для йоги, нескользящий"))

        self.bundles["office_workspace"] = bundle
        return bundle

    def create_clothing_bundle(self) -> ProductComposite:
        bundle = ProductComposite("Спортивный набор", "Для активного отдыха")

        bundle.add(ProductLeaf(21, "Велосипед горный", Decimal('29999.99'), "Горный велосипед, 26 дюймов"))
        bundle.add(ProductLeaf(22, "Гантели 5кг", Decimal('1499.99'), "Пара гантелей по 5 кг"))
        bundle.add(ProductLeaf(24, "Мяч футбольный", Decimal('1999.99'), "Футбольный мяч, размер 5"))

        self.bundles["casual_outfit"] = bundle
        return bundle