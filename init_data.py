from database import SessionLocal, Category, Product, Decorator


def init_database():
    db = SessionLocal()

    try:
        # Проверяем, есть ли уже категории
        existing_categories = db.query(Category).count()
        if existing_categories == 0:
            categories = [
                Category(name="Электроника"),
                Category(name="Одежда"),
                Category(name="Бытовая техника"),
                Category(name="Книги"),
                Category(name="Спорт и отдых")
            ]

            for category in categories:
                db.add(category)
            db.commit()
            print("Категории успешно добавлены")

        # Проверяем, есть ли уже товары
        existing_products = db.query(Product).count()
        if existing_products == 0:
            products = [
                # Электроника
                Product(category_id=1, name="Смартфон Galaxy S23", price=59999.99,
                        description="Смартфон Samsung Galaxy S23, 256GB, черный"),
                Product(category_id=1, name="Ноутбук ASUS ROG", price=124999.99,
                        description="Игровой ноутбук ASUS ROG Strix, 16GB RAM, 512GB SSD"),
                Product(category_id=1, name="Наушники AirPods Pro", price=18999.99,
                        description="Беспроводные наушники Apple AirPods Pro с шумоподавлением"),

                # Одежда
                Product(category_id=2, name="Футболка классическая", price=1999.99,
                        description="Хлопковая футболка, белая, размер M"),
                Product(category_id=2, name="Джинсы прямые", price=3999.99,
                        description="Классические джинсы, синие, размер 32"),
                Product(category_id=2, name="Кроссовки Nike", price=6999.99,
                        description="Спортивные кроссовки Nike Air Max, 42 размер"),

                # Бытовая техника
                Product(category_id=3, name="Блендер Philips", price=4999.99,
                        description="Мощный блендер Philips HR3556, 700W"),
                Product(category_id=3, name="Пылесос Dyson", price=29999.99,
                        description="Беспроводной пылесос Dyson V15"),

                # Книги
                Product(category_id=4, name="Война и мир", price=999.99,
                        description="Лев Толстой, роман-эпопея, твердый переплет"),
                Product(category_id=4, name="Преступление и наказание", price=799.99,
                        description="Федор Достоевский, классический роман"),

                # Спорт и отдых
                Product(category_id=5, name="Велосипед горный", price=29999.99,
                        description="Горный велосипед, 26 дюймов, 21 скорость"),
                Product(category_id=5, name="Гантели 5кг", price=1499.99,
                        description="Пара гантелей по 5 кг, резиновое покрытие"),
            ]

            for product in products:
                db.add(product)
            db.commit()
            print("Товары успешно добавлены")

        # Проверяем, есть ли уже декораторы
        existing_decorators = db.query(Decorator).count()
        if existing_decorators == 0:
            decorators = [
                Decorator(name="Подарочная упаковка", cost=199.00),
                Decorator(name="Срочная доставка", cost=499.00),
                Decorator(name="Персонализация (гравировка)", cost=299.00),
                Decorator(name="Страхование товара", cost=249.00),
                Decorator(name="Расширенная гарантия", cost=999.00),
                Decorator(name="Поздравительная открытка", cost=99.00),
            ]

            for decorator in decorators:
                db.add(decorator)
            db.commit()
            print("Декораторы успешно добавлены")

        print("Инициализация базы данных успешно завершена!")

    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()