# fix_database.py
from database import SessionLocal, Base, engine
from sqlalchemy import text


def check_and_fix_database():
    db = SessionLocal()
    try:
        print("Проверка структуры базы данных...")

        # Проверяем существование таблиц
        tables = ['category', 'product', 'decorators', 'orders', 'order_items', 'order_decorators']

        for table in tables:
            result = db.execute(
                text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')"))
            exists = result.scalar()
            print(f"Таблица {table}: {'СУЩЕСТВУЕТ' if exists else 'ОТСУТСТВУЕТ'}")

        # Проверяем данные в категориях
        result = db.execute(text("SELECT COUNT(*) FROM category"))
        category_count = result.scalar()
        print(f"Количество категорий: {category_count}")

        # Проверяем данные в товарах
        result = db.execute(text("SELECT COUNT(*) FROM product"))
        product_count = result.scalar()
        print(f"Количество товаров: {product_count}")

        # Если категорий нет, добавляем
        if category_count == 0:
            print("Добавляем категории...")
            db.execute(text("INSERT INTO category (name) VALUES ('Electronics'), ('Clothing'), ('Home Appliances')"))
            db.commit()
            print("Категории добавлены")

        # Если товаров нет, добавляем
        if product_count == 0:
            print("Добавляем товары...")
            products = [
                (1, 'Smartphone', 499.99, 'Latest smartphone with advanced features'),
                (1, 'Laptop', 899.99, 'High-performance laptop for work and gaming'),
                (1, 'Headphones', 149.99, 'Wireless noise-canceling headphones'),
                (2, 'T-Shirt', 19.99, 'Comfortable cotton t-shirt'),
                (2, 'Jeans', 39.99, 'Classic denim jeans'),
                (2, 'Jacket', 79.99, 'Warm winter jacket'),
                (3, 'Blender', 49.99, 'Powerful kitchen blender'),
                (3, 'Vacuum Cleaner', 129.99, 'Efficient vacuum cleaner'),
            ]

            for category_id, name, price, description in products:
                db.execute(
                    text(
                        "INSERT INTO product (category_id, name, price, description) VALUES (:category_id, :name, :price, :description)"),
                    {"category_id": category_id, "name": name, "price": price, "description": description}
                )

            db.commit()
            print("Товары добавлены")

        # Проверяем декораторы
        result = db.execute(text("SELECT COUNT(*) FROM decorators"))
        decorator_count = result.scalar()
        print(f"Количество декораторов: {decorator_count}")

        if decorator_count == 0:
            print("Добавляем декораторы...")
            db.execute(text(
                "INSERT INTO decorators (name, cost) VALUES ('Gift Wrap', 5.00), ('Express Shipping', 15.00), ('Personalization', 10.00), ('Insurance', 7.50)"))
            db.commit()
            print("Декораторы добавлены")

        print("Проверка базы данных завершена!")

    except Exception as e:
        print(f"Ошибка при проверке базы данных: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    check_and_fix_database()