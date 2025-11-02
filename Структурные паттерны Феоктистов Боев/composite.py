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
        return "  " * indent + f"Product: {self.name} - ${self.price}"


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
        result = "  " * indent + f"Bundle: {self.name} (Total: ${self.get_price()})\n"
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
        bundle = ProductComposite("Gaming Computer Bundle", "Complete gaming setup")

        bundle.add(ProductLeaf(1, "Gaming PC", Decimal('999.99'), "High-performance gaming computer"))
        bundle.add(ProductLeaf(2, "27-inch Monitor", Decimal('299.99'), "4K gaming monitor"))
        bundle.add(ProductLeaf(3, "Mechanical Keyboard", Decimal('89.99'), "RGB mechanical keyboard"))
        bundle.add(ProductLeaf(4, "Gaming Mouse", Decimal('49.99'), "Precision gaming mouse"))

        self.bundles["gaming_computer"] = bundle
        return bundle

    def create_office_bundle(self) -> ProductComposite:
        bundle = ProductComposite("Office Workspace Bundle", "Complete office setup")

        bundle.add(ProductLeaf(5, "Office Desk", Decimal('199.99'), "Ergonomic office desk"))
        bundle.add(ProductLeaf(6, "Office Chair", Decimal('149.99'), "Comfortable office chair"))
        bundle.add(ProductLeaf(7, "Desk Lamp", Decimal('29.99'), "LED desk lamp"))

        self.bundles["office_workspace"] = bundle
        return bundle

    def create_clothing_bundle(self) -> ProductComposite:
        bundle = ProductComposite("Casual Outfit Bundle", "Complete casual outfit")

        bundle.add(ProductLeaf(8, "T-Shirt", Decimal('19.99'), "Cotton t-shirt"))
        bundle.add(ProductLeaf(9, "Jeans", Decimal('39.99'), "Classic jeans"))
        bundle.add(ProductLeaf(10, "Sneakers", Decimal('59.99'), "Comfortable sneakers"))

        self.bundles["casual_outfit"] = bundle
        return bundle