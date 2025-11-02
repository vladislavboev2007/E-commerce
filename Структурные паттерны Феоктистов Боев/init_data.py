from database import SessionLocal, Category, Product, Decorator


def init_database():
    db = SessionLocal()

    try:
        # Проверяем, есть ли уже категории
        existing_categories = db.query(Category).count()
        if existing_categories == 0:
            # Категории
            categories = [
                Category(name="Electronics"),
                Category(name="Clothing"),
                Category(name="Home Appliances")
            ]

            for category in categories:
                db.add(category)
            db.commit()
            print("Categories added successfully")
        else:
            print(f"Categories already exist ({existing_categories} categories found)")

        # Проверяем, есть ли уже товары
        existing_products = db.query(Product).count()
        if existing_products == 0:
            # Товары
            products = [
                Product(category_id=1, name="Smartphone", price=499.99,
                        description="Latest smartphone with advanced features"),
                Product(category_id=1, name="Laptop", price=899.99,
                        description="High-performance laptop for work and gaming"),
                Product(category_id=1, name="Headphones", price=149.99,
                        description="Wireless noise-canceling headphones"),
                Product(category_id=1, name="Smart Watch", price=199.99,
                        description="Feature-rich smartwatch with health monitoring"),

                Product(category_id=2, name="T-Shirt", price=19.99, description="Comfortable cotton t-shirt"),
                Product(category_id=2, name="Jeans", price=39.99, description="Classic denim jeans"),
                Product(category_id=2, name="Jacket", price=79.99, description="Warm winter jacket"),
                Product(category_id=2, name="Sneakers", price=59.99, description="Comfortable running sneakers"),

                Product(category_id=3, name="Blender", price=49.99, description="Powerful kitchen blender"),
                Product(category_id=3, name="Vacuum Cleaner", price=129.99, description="Efficient vacuum cleaner"),
                Product(category_id=3, name="Coffee Maker", price=89.99, description="Automatic coffee maker"),
                Product(category_id=3, name="Microwave", price=99.99, description="Compact microwave oven"),
            ]

            for product in products:
                db.add(product)
            db.commit()
            print("Products added successfully")
        else:
            print(f"Products already exist ({existing_products} products found)")

        # Проверяем, есть ли уже декораторы
        existing_decorators = db.query(Decorator).count()
        if existing_decorators == 0:
            # Декораторы
            decorators = [
                Decorator(name="Gift Wrap", cost=5.00),
                Decorator(name="Express Shipping", cost=15.00),
                Decorator(name="Personalization", cost=10.00),
                Decorator(name="Insurance", cost=7.50),
            ]

            for decorator in decorators:
                db.add(decorator)
            db.commit()
            print("Decorators added successfully")
        else:
            print(f"Decorators already exist ({existing_decorators} decorators found)")

        print("Database initialization completed successfully!")

    except Exception as e:
        print(f"Error during database initialization: {e}")
        db.rollback()
    finally:
        db.close()


def clear_database():
    """Функция для очистки базы данных (использовать с осторожностью!)"""
    db = SessionLocal()
    try:
        # Удаляем в правильном порядке из-за foreign key constraints
        db.query(Decorator).delete()
        db.query(Product).delete()
        db.query(Category).delete()
        db.commit()
        print("Database cleared successfully!")
    except Exception as e:
        print(f"Error clearing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()