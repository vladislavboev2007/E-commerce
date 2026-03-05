# E-Commerce Web Application with Structural Design Patterns

## Project Description

A modern e-commerce web application built with Python FastAPI that demonstrates the implementation of three fundamental structural design patterns: **Adapter**, **Decorator**, and **Composite**.

## 🛍️ What is E-Commerce?

E-commerce (electronic commerce) refers to the buying and selling of goods and services over the internet. This web application simulates a real online store where users can:

- **Browse products** across different categories (Электроника, Одежда, Бытовая техника, Книги, Спорт и отдых)
- **Add items to shopping cart** with dynamic price calculations in Russian Rubles (₽)
- **Apply additional services** like gift wrapping, express shipping, personalization, and extended warranty
- **Purchase product bundles** as complete sets
- **Process payments** through Russian payment providers (ЮKassa, Сбер)
- **Schedule deliveries** with Russian shipping services (СДЭК, Яндекс.Маркет)

## 🏗️ Structural Design Patterns Implemented

### 1. **Adapter Pattern**
- **Purpose**: Integrate external services with incompatible APIs
- **Implementation**: 
  - Payment services (ЮKassa, Сбер) with different interfaces
  - Delivery services (СДЭК, Яндекс.Маркет) with varying data formats
- **Files**: `adapters.py`

### 2. **Decorator Pattern**
- **Purpose**: Dynamically add features to products without modifying their structure
- **Implementation**:
  - Additional services: Подарочная упаковка, Срочная доставка, Персонализация (гравировка), Страхование товара, Расширенная гарантия, Поздравительная открытка
  - Real-time price updates when services are selected
- **Files**: `decorators.py`

### 3. **Composite Pattern**
- **Purpose**: Treat individual products and product bundles uniformly
- **Implementation**:
  - Create ready-made bundles (Игровой компьютер, Офисный набор, Спортивный набор)
  - Calculate total prices for bundles as single entities
- **Files**: `composite.py`

## 🚀 Features

- **Product Catalog** with categories and search functionality
- **Shopping Cart** with quantity management
- **Dynamic Pricing** with decorator pattern
- **Product Bundles** using composite pattern
- **Payment Processing** via multiple adapters (ЮKassa, Сбер)
- **Delivery Management** with multiple providers (СДЭК, Яндекс.Маркет)
- **Order Management** with status tracking
- **Responsive UI** with modern design and mobile adaptation

## 💻 Technology Stack

- **Backend**: Python 3.7+, FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Architecture**: REST API with structural design patterns
- **Tools**: Git, Uvicorn, Pydantic

## 📋 Database Schema

The application uses PostgreSQL with the following tables:
- **category** - product categories
- **product** - products with prices in rubles
- **decorators** - additional services
- **orders** - customer orders
- **order_items** - products in orders
- **order_decorators** - services in orders

## 📁 Project Structure
<img width="312" height="576" alt="image" src="https://github.com/user-attachments/assets/ece989f0-2c6c-4da6-9c0f-037257964b49" />


## 🎯 Educational Value

This project serves as a practical example of how structural design patterns can be applied in real-world e-commerce applications to create:

- **Scalable architecture** that can easily integrate new services
- **Maintainable code** with clear separation of concerns
- **Flexible functionality** that can be extended without breaking existing code
- **Professional software design** following industry best practices

## 🌟 Key Improvements

- **Russian Localization**: Full support for Russian language, currency (₽), and payment/delivery providers
- **Extended Decorators**: 6 additional services with fixed pricing
- **Enhanced Categories**: 5 categories with custom emoji icons (📱, 👕, 🖥, 📔, 🎾)
- **Realistic Pricing**: Updated product prices in Russian Rubles
- **Responsive Design**: Mobile-friendly interface with adaptive layouts

Perfect for understanding how design patterns solve common software architecture problems in commercial web applications with regional adaptation!

## 🚦 Installation and Setup
**Prerequisites**
- Python 3.12 or higher
- PostgreSQL database
- pip (Python package manager)

**Step 1: Clone the Repository**
```bash
git clone https://github.com/vladislavboev2007/E-commerce.git
cd "E-commerce"
```
Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```
Step 3: Configure Database
Create a PostgreSQL database and load the schema and data from database/backup.sql using Plain format:

```sql
CREATE DATABASE "E-commerce";
```
Update the connection string in database.py:

```python
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/E-commerce")
```
Step 4: Initialize Database with Test Data
bash
python init_data.py
This will populate the database with:

* Categories (Электроника, Одежда, Бытовая техника, Книги, Спорт и отдых)
* Products with realistic prices in Russian Rubles
* Decorators (additional services) with fixed costs

Step 5: Start the Application
```bash
uvicorn main:app --reload
```
or

```bash
python main.py
```
The application will be available at: http://127.0.0.1:8000

Step 6: Run Unit Tests (Optional)
```bash
python test_app.py
```
## ⚠️ Troubleshooting
Issue: Data not loading (Products/Categories not displayed)
Solutions:

Check Port Configuration

Verify that the port in static/js/common.js matches the port where the server is running

Default server port: 8000

Update if different:

```javascript
// static/js/common.js
const API_BASE = 'http://localhost:8000/api';  // Change 8000 to your actual port
```
Hard Refresh Browser Cache

Press Ctrl+F5 (Windows/Linux) or Cmd+Shift+R (Mac)

This forces the browser to reload all resources including the updated JavaScript

Restart the Application

```bash
# Stop the server (Ctrl+C)
python main.py
```