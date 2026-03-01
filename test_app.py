import unittest
import os
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Импорты приложения
from main import app, get_db
from database import Base, Product, Category, Decorator


# Настройки PostgreSQL для тестов
# Используем отдельную тестовую базу данных
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:1234@localhost:5432/E-commerce_test"  # отдельная тестовая БД
)

# Создаем подключение к PostgreSQL
engine = create_engine(TEST_DATABASE_URL)

# Создаем таблицы в тестовой БД
Base.metadata.drop_all(bind=engine)  # очищаем старые таблицы
Base.metadata.create_all(bind=engine)  # создаем новые

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределение зависимости БД для тестов"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestECommerceAppPostgreSQL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создание структуры БД один раз для всех тестов"""
        print("Подключение к PostgreSQL")
        print(f"База данных: {TEST_DATABASE_URL}")

        # Проверяем подключение
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("Подключение к PostgreSQL успешно")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            raise

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом"""
        self.db = TestingSessionLocal()

        # Очищаем таблицы в правильном порядке
        self.db.execute(text("DELETE FROM order_decorators"))
        self.db.execute(text("DELETE FROM order_items"))
        self.db.execute(text("DELETE FROM orders"))
        self.db.execute(text("DELETE FROM decorators"))
        self.db.execute(text("DELETE FROM product"))
        self.db.execute(text("DELETE FROM category"))
        self.db.commit()

        # Создаем категорию
        self.db.execute(
            text("INSERT INTO category (id, name) VALUES (1, 'Электроника')")
        )
        self.db.commit()

        # Создаем товар
        self.db.execute(
            text("""
                INSERT INTO product (id, category_id, name, price, description) 
                VALUES (1, 1, 'Тестовый смартфон', 29999.99, 'Тестовое описание')
            """)
        )
        self.db.commit()

        # Создаем декораторы
        decorators_data = [
            (1, 'Подарочная упаковка', 199.00),
            (2, 'Срочная доставка', 499.00),
            (3, 'Страхование товара', 249.00),
        ]
        for id, name, cost in decorators_data:
            self.db.execute(
                text("INSERT INTO decorators (id, name, cost) VALUES (:id, :name, :cost)"),
                {"id": id, "name": name, "cost": cost}
            )
        self.db.commit()

        self.product_id = 1
        print(f"\n Тестовые данные созданы в PostgreSQL")

    def tearDown(self):
        """Очистка после каждого теста"""
        self.db.close()

    # Тест 1: Позитивный
    def test_1_create_order_success(self):
        print("Тест 1: Создание заказа (позитивный)")

        order_data = {
            "user_id": 1,
            "items": [{"product_id": self.product_id, "quantity": 2}],
            "decorators": ["Подарочная упаковка", "Страхование товара"]
        }

        print(f"Отправка заказа: товар ID {self.product_id}, количество 2")
        print(f"Услуги: Подарочная упаковка (199₽), Страхование товара (249₽)")

        response = client.post("/api/orders/", json=order_data)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        print(f"Статус ответа: {response.status_code}")
        print(f"Данные ответа: {data}")

        # Проверка расчетов
        items_amount = float(data["items_amount"])
        decorators_amount = float(data["decorators_amount"])
        final_amount = float(data["final_amount"])

        self.assertAlmostEqual(items_amount, 59999.98, places=2)
        self.assertAlmostEqual(decorators_amount, 448.00, places=2)
        self.assertAlmostEqual(final_amount, 60447.98, places=2)

        print(f"Сумма товаров: {items_amount}₽")
        print(f"Сумма услуг: {decorators_amount}₽")
        print(f"Итого: {final_amount}₽")
        print("Тест 1 пройден")
        print("")

    # Тест 2: Негативный
    def test_2_create_order_product_not_found(self):
        print("\n" + "="*50)
        print("Тест 2: Заказ несуществующего товара (негативный)")
        print("="*50)

        order_data = {
            "user_id": 1,
            "items": [{"product_id": 99999, "quantity": 1}],
            "decorators": []
        }

        print(f"Отправка заказа с несуществующим ID товара: 99999")

        response = client.post("/api/orders/", json=order_data)

        print(f"Код ответа: {response.status_code}")

        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("detail", data)

        print(f"Сообщение об ошибке: {data['detail']}")
        print("Тест 2 пройден (ожидаемая ошибка 404 получена)")

    # Тест 3: Негативный
    def test_3_payment_unsupported_provider(self):
        print("Тест 3: Неподдерживаемый способ оплаты (негативный)")

        payment_data = {
            "order_id": 1,
            "payment_provider": "bitcoin",
            "amount": 1000.00
        }

        print(f"Отправка запроса с неподдерживаемым провайдером: bitcoin")

        response = client.post("/api/payment/process/", json=payment_data)

        print(f"Код ответа: {response.status_code}")

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("detail", data)

        print(f"Сообщение об ошибке: {data['detail']}")
        print("Тест 3 пройден (ожидаемая ошибка 400 получена)")


if __name__ == "__main__":

    print("Модульное тестирование")

    unittest.main(verbosity=2, failfast=True)