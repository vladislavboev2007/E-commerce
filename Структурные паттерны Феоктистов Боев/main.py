# main.py
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from decimal import Decimal
import uuid
import os

from database import SessionLocal, engine, Base, Product, Category, Order, OrderItem, Decorator, OrderDecorator
from adapters import (
    StripePaymentAdapter, PayPalPaymentAdapter,
    DHLDeliveryAdapter, FedExDeliveryAdapter
)
from decorators import BaseProduct, DecoratorManager
from composite import CatalogManager, ProductLeaf, ProductComposite

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API", version="1.0.0")

# Настройка статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Зависимость БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Инициализация менеджеров
decorator_manager = DecoratorManager()
catalog_manager = CatalogManager()

# Pydantic модели
from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    description: str
    category_name: str


class DecoratorResponse(BaseModel):
    id: int
    name: str
    cost: Decimal


class OrderCreate(BaseModel):
    user_id: int
    items: List[dict]
    decorators: List[str] = []
    personalization_text: Optional[str] = None


class PaymentRequest(BaseModel):
    order_id: int
    payment_provider: str
    amount: Decimal


class DeliveryRequest(BaseModel):
    order_id: int
    delivery_provider: str
    shipping_address: dict


# HTML страницы
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/products", response_class=HTMLResponse)
async def read_products(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})


@app.get("/product", response_class=HTMLResponse)
async def read_product(request: Request):
    return templates.TemplateResponse("product.html", {"request": request})


@app.get("/bundles", response_class=HTMLResponse)
async def read_bundles(request: Request):
    return templates.TemplateResponse("bundles.html", {"request": request})


@app.get("/cart", response_class=HTMLResponse)
async def read_cart(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})


@app.get("/checkout", response_class=HTMLResponse)
async def read_checkout(request: Request):
    return templates.TemplateResponse("checkout.html", {"request": request})


@app.get("/orders", response_class=HTMLResponse)
async def read_orders(request: Request):
    return templates.TemplateResponse("orders.html", {"request": request})

@app.get("/api/test")
async def test_api():
    return {"message": "API is working", "status": "ok"}


# API endpoints
@app.get("/api/categories/", response_model=List[dict])
async def get_categories(db: Session = Depends(get_db)):
    try:
        categories = db.query(Category).all()
        print(f"Найдено категорий: {len(categories)}")
        return [{"id": cat.id, "name": cat.name} for cat in categories]
    except Exception as e:
        print(f"Ошибка в get_categories: {e}")
        import traceback
        traceback.print_exc()
        return []


@app.get("/api/products/", response_model=List[ProductResponse])
async def get_products(
        db: Session = Depends(get_db),
        category_id: Optional[int] = Query(None),
        search: Optional[str] = Query(None),
        limit: Optional[int] = Query(None)
):
    try:
        # Используем joinedload для загрузки связанных категорий
        query = db.query(Product).options(joinedload(Product.category))

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))

        if limit:
            query = query.limit(limit)

        products = query.all()
        print(f"Найдено товаров: {len(products)}")

        result = []
        for product in products:
            # Проверяем, что категория загружена
            category_name = product.category.name if product.category else "Unknown"

            result.append(ProductResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                description=product.description or "",
                category_name=category_name
            ))

        return result

    except Exception as e:
        print(f"Ошибка в get_products: {e}")
        import traceback
        traceback.print_exc()
        return []


@app.get("/api/decorators/", response_model=List[DecoratorResponse])
async def get_decorators(db: Session = Depends(get_db)):
    decorators = db.query(Decorator).all()
    return [
        DecoratorResponse(
            id=decorator.id,
            name=decorator.name,
            cost=decorator.cost
        )
        for decorator in decorators
    ]


@app.post("/api/calculate-price/")
async def calculate_price(product_data: dict, db: Session = Depends(get_db)):
    try:
        print("Received product data:", product_data)

        base_price = Decimal(str(product_data["base_price"]))
        quantity = product_data.get("quantity", 1)
        decorators = product_data.get("decorators", [])

        # Рассчитываем базовую стоимость товаров
        base_total = base_price * quantity

        # Создаем базовый продукт с общей стоимостью товаров
        base_product = BaseProduct(
            product_id=product_data["product_id"],
            name=product_data["name"],
            base_price=base_total,  # Передаем общую стоимость товаров
            description=product_data.get("description", "")
        )

        # Применяем декораторы (они добавят фиксированные суммы)
        kwargs = {}
        if "Personalization" in decorators and product_data.get("personalization_text"):
            kwargs["personalization_text"] = product_data["personalization_text"]

        decorated_product = decorator_manager.apply_decorators(
            base_product, decorators, **kwargs
        )

        final_total = decorated_product.get_price()
        decorators_total = final_total - base_total

        print(f"Calculation: base_price={base_price}, quantity={quantity}, decorators={decorators}")
        print(f"Result: base_total={base_total}, decorators_total={decorators_total}, final_total={final_total}")

        return {
            "base_total": float(base_total),
            "decorators_total": float(decorators_total),
            "final_price": float(final_total),
            "description": decorated_product.get_description()
        }
    except Exception as e:
        print(f"Error in calculate-price: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/bundles/")
async def get_bundles():
    gaming_bundle = catalog_manager.create_computer_bundle()
    office_bundle = catalog_manager.create_office_bundle()
    clothing_bundle = catalog_manager.create_clothing_bundle()

    return {
        "bundles": {
            "gaming_computer": {
                "name": gaming_bundle.name,
                "description": gaming_bundle.description,
                "total_price": float(gaming_bundle.get_price()),
                "display": gaming_bundle.display()
            },
            "office_workspace": {
                "name": office_bundle.name,
                "description": office_bundle.description,
                "total_price": float(office_bundle.get_price()),
                "display": office_bundle.display()
            },
            "casual_outfit": {
                "name": clothing_bundle.name,
                "description": clothing_bundle.description,
                "total_price": float(clothing_bundle.get_price()),
                "display": clothing_bundle.display()
            }
        }
    }


@app.post("/api/orders/")
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    order = Order(
        user_id=order_data.user_id,
        total_amount=Decimal('0.00')
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    total_amount = Decimal('0.00')
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item['product_id']} not found")

        subtotal = product.price * item["quantity"]
        total_amount += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            subtotal=subtotal
        )
        db.add(order_item)

    # Добавляем фиксированную стоимость декораторов
    decorators_total = Decimal('0.00')
    if order_data.decorators:
        decorators = db.query(Decorator).filter(Decorator.name.in_(order_data.decorators)).all()
        for decorator in decorators:
            decorators_total += decorator.cost
            order_decorator = OrderDecorator(
                order_id=order.id,
                decorator_id=decorator.id
            )
            db.add(order_decorator)

    # Итоговая сумма = стоимость товаров + фиксированная стоимость услуг
    order.total_amount = total_amount + decorators_total
    db.commit()

    return {
        "order_id": order.id,
        "items_amount": float(total_amount),
        "decorators_amount": float(decorators_total),
        "final_amount": float(order.total_amount),
        "description": f"Товары: ${total_amount}, Услуги: ${decorators_total}"
    }


@app.post("/api/payment/process/")
async def process_payment(payment_data: PaymentRequest):
    if payment_data.payment_provider == "stripe":
        adapter = StripePaymentAdapter()
    elif payment_data.payment_provider == "paypal":
        adapter = PayPalPaymentAdapter()
    else:
        raise HTTPException(status_code=400, detail="Unsupported payment provider")

    order_data = {
        "order_id": payment_data.order_id,
        "user_id": 1,
        "amount": payment_data.amount
    }

    result = adapter.process_payment(float(payment_data.amount), order_data)
    return result


@app.post("/api/delivery/schedule/")
async def schedule_delivery(delivery_data: DeliveryRequest):
    if delivery_data.delivery_provider == "dhl":
        adapter = DHLDeliveryAdapter()
    elif delivery_data.delivery_provider == "fedex":
        adapter = FedExDeliveryAdapter()
    else:
        raise HTTPException(status_code=400, detail="Unsupported delivery provider")

    order_data = {
        "order_id": delivery_data.order_id,
        "shipping_address": delivery_data.shipping_address
    }

    result = adapter.schedule_delivery(order_data)
    return result

@app.get("/api/debug/products")
async def debug_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {
        "total_products": len(products),
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": float(p.price),
                "category_id": p.category_id
            }
            for p in products
        ]
    }

@app.get("/api/debug/categories")
async def debug_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return {
        "total_categories": len(categories),
        "categories": [{"id": c.id, "name": c.name} for c in categories]
    }


@app.get("/api/create-test-data")
async def create_test_data(db: Session = Depends(get_db)):
    """Создает тестовые данные если их нет"""
    try:
        # Проверяем и создаем категории
        if db.query(Category).count() == 0:
            categories = [
                Category(name="Electronics"),
                Category(name="Clothing"),
                Category(name="Home Appliances")
            ]
            db.add_all(categories)
            db.commit()

        # Проверяем и создаем товары
        if db.query(Product).count() == 0:
            products = [
                Product(category_id=1, name="Smartphone", price=499.99, description="Latest smartphone"),
                Product(category_id=1, name="Laptop", price=899.99, description="High-performance laptop"),
                Product(category_id=1, name="Headphones", price=149.99, description="Wireless headphones"),
                Product(category_id=2, name="T-Shirt", price=19.99, description="Cotton t-shirt"),
                Product(category_id=2, name="Jeans", price=39.99, description="Classic jeans"),
                Product(category_id=3, name="Blender", price=49.99, description="Kitchen blender"),
                Product(category_id=3, name="Vacuum Cleaner", price=129.99, description="Powerful vacuum"),
            ]
            db.add_all(products)
            db.commit()

        # Проверяем и создаем декораторы
        if db.query(Decorator).count() == 0:
            decorators = [
                Decorator(name="Gift Wrap", cost=5.00),
                Decorator(name="Express Shipping", cost=15.00),
                Decorator(name="Personalization", cost=10.00),
                Decorator(name="Insurance", cost=7.50),
            ]
            db.add_all(decorators)
            db.commit()

        return {"message": "Test data created successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


@app.get("/api/debug/database")
async def debug_database(db: Session = Depends(get_db)):
    """Endpoint для отладки структуры базы данных"""
    from sqlalchemy import text

    try:
        # Проверяем таблицы
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result]

        # Проверяем данные в основных таблицах
        categories_count = db.execute(text("SELECT COUNT(*) FROM category")).scalar()
        products_count = db.execute(text("SELECT COUNT(*) FROM product")).scalar()
        decorators_count = db.execute(text("SELECT COUNT(*) FROM decorators")).scalar()
        orders_count = db.execute(text("SELECT COUNT(*) FROM orders")).scalar()

        # Получаем несколько товаров с категориями
        products_with_categories = db.execute(text("""
            SELECT p.id, p.name, p.price, c.name as category_name
            FROM product p
            LEFT JOIN category c ON p.category_id = c.id
            LIMIT 5
        """)).fetchall()

        return {
            "tables": tables,
            "counts": {
                "categories": categories_count,
                "products": products_count,
                "decorators": decorators_count,
                "orders": orders_count
            },
            "sample_products": [
                {
                    "id": row[0],
                    "name": row[1],
                    "price": float(row[2]) if row[2] else 0,
                    "category": row[3]
                }
                for row in products_with_categories
            ]
        }
    except Exception as e:
        return {"error": str(e)}


def get_order_status(order):
    """Определяет статус заказа на основе даты создания"""
    from datetime import datetime, timedelta

    if not order.created_at:
        return "Неизвестно"

    try:
        # Преобразуем в наивный datetime для сравнения
        now = datetime.now()
        order_date = order.created_at

        # Если есть информация о часовом поясе, убираем ее
        if order_date.tzinfo is not None:
            order_date = order_date.replace(tzinfo=None)
        if now.tzinfo is not None:
            now = now.replace(tzinfo=None)

        order_age = now - order_date

        if order_age > timedelta(days=7):
            return "Доставлен"
        elif order_age > timedelta(days=2):
            return "Доставляется"
        else:
            return "В обработке"
    except Exception as e:
        print(f"Error calculating order status: {e}")
        return "Неизвестно"

@app.get("/api/user-orders/")
async def get_user_orders(db: Session = Depends(get_db)):
    """Получение заказов пользователя"""
    try:
        # Используем user_id = 1 для демо, но покажем все заказы для отладки
        user_id = 1

        orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()

        print(f"Found {len(orders)} orders for user {user_id}")  # Для отладки

        orders_data = []
        for order in orders:
            # Получаем товары заказа
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
            items_data = []
            for item in order_items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                items_data.append({
                    "name": product.name if product else "Unknown Product",
                    "quantity": item.quantity,
                    "price": float(item.subtotal / item.quantity) if item.quantity > 0 else 0
                })

            # Получаем декораторы заказа
            order_decorators = db.query(OrderDecorator).filter(OrderDecorator.order_id == order.id).all()
            decorators_data = []
            for decorator_rel in order_decorators:
                decorator = db.query(Decorator).filter(Decorator.id == decorator_rel.decorator_id).first()
                if decorator:
                    decorators_data.append(decorator.name)

            orders_data.append({
                "id": order.id,
                "order_date": order.created_at.strftime("%Y-%m-%d") if order.created_at else "Unknown",
                "total_amount": float(order.total_amount),
                "status": get_order_status(order),  # Функция для определения статуса
                "items": items_data,
                "decorators": decorators_data
            })

        return orders_data

    except Exception as e:
        print(f"Error getting user orders: {e}")
        import traceback
        traceback.print_exc()
        return []


@app.get("/api/debug/orders")
async def debug_orders(db: Session = Depends(get_db)):
    """Отладка заказов"""
    try:
        orders = db.query(Order).all()
        orders_data = []

        for order in orders:
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
            items_data = []

            for item in order_items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                items_data.append({
                    "product_id": item.product_id,
                    "product_name": product.name if product else "Unknown",
                    "quantity": item.quantity,
                    "subtotal": float(item.subtotal)
                })

            orders_data.append({
                "id": order.id,
                "user_id": order.user_id,
                "total_amount": float(order.total_amount),
                "created_at": str(order.created_at),
                "items_count": len(order_items),
                "items": items_data
            })

        return {
            "total_orders": len(orders),
            "orders": orders_data
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)