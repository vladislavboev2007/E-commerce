# decorators.py
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List


class ProductComponent(ABC):
    @abstractmethod
    def get_price(self) -> Decimal:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class BaseProduct(ProductComponent):
    def __init__(self, product_id: int, name: str, base_price: Decimal, description: str):
        self.product_id = product_id
        self.name = name
        self.base_price = base_price
        self.base_description = description

    def get_price(self) -> Decimal:
        return self.base_price

    def get_description(self) -> str:
        return self.base_description


class ProductDecorator(ProductComponent):
    def __init__(self, product: ProductComponent):
        self._product = product

    def get_price(self) -> Decimal:
        return self._product.get_price()

    def get_description(self) -> str:
        return self._product.get_description()


class GiftWrapDecorator(ProductDecorator):
    def __init__(self, product: ProductComponent, wrap_cost: Decimal = Decimal('5.00')):
        super().__init__(product)
        self.wrap_cost = wrap_cost

    def get_price(self) -> Decimal:
        # ФИКСИРОВАННАЯ стоимость - не зависит от количества
        return self._product.get_price() + self.wrap_cost

    def get_description(self) -> str:
        return f"{self._product.get_description()} + Gift Wrap (${self.wrap_cost})"


class ExpressShippingDecorator(ProductDecorator):
    def __init__(self, product: ProductComponent, shipping_cost: Decimal = Decimal('15.00')):
        super().__init__(product)
        self.shipping_cost = shipping_cost

    def get_price(self) -> Decimal:
        # ФИКСИРОВАННАЯ стоимость - не зависит от количества
        return self._product.get_price() + self.shipping_cost

    def get_description(self) -> str:
        return f"{self._product.get_description()} + Express Shipping (${self.shipping_cost})"


class PersonalizationDecorator(ProductDecorator):
    def __init__(self, product: ProductComponent, personalization_text: str,
                 personalization_cost: Decimal = Decimal('10.00')):
        super().__init__(product)
        self.personalization_text = personalization_text
        self.personalization_cost = personalization_cost

    def get_price(self) -> Decimal:
        # ФИКСИРОВАННАЯ стоимость - не зависит от количества
        return self._product.get_price() + self.personalization_cost

    def get_description(self) -> str:
        return f"{self._product.get_description()} + Personalization: '{self.personalization_text}' (${self.personalization_cost})"


class InsuranceDecorator(ProductDecorator):
    def __init__(self, product: ProductComponent, insurance_cost: Decimal = Decimal('7.50')):
        super().__init__(product)
        self.insurance_cost = insurance_cost

    def get_price(self) -> Decimal:
        # ФИКСИРОВАННАЯ стоимость - не зависит от количества
        return self._product.get_price() + self.insurance_cost

    def get_description(self) -> str:
        return f"{self._product.get_description()} + Insurance (${self.insurance_cost})"
class DecoratorManager:
    def __init__(self):
        self.decorators = {
            "Gift Wrap": GiftWrapDecorator,
            "Express Shipping": ExpressShippingDecorator,
            "Personalization": PersonalizationDecorator,
            "Insurance": InsuranceDecorator
        }

    def apply_decorators(self, base_product: BaseProduct, decorator_types: List[str], **kwargs) -> ProductComponent:
        decorated_product = base_product

        for decorator_type in decorator_types:
            if decorator_type in self.decorators:
                if decorator_type == "Personalization":
                    decorated_product = self.decorators[decorator_type](
                        decorated_product,
                        kwargs.get("personalization_text", "")
                    )
                else:
                    decorated_product = self.decorators[decorator_type](decorated_product)

        return decorated_product