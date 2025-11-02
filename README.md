# E-Commerce Web Application with Structural Design Patterns

## Project Description

A modern e-commerce web application built with Python FastAPI that demonstrates the implementation of three fundamental structural design patterns: **Adapter**, **Decorator**, and **Composite**.

## 🛍️ What is E-Commerce?

E-commerce (electronic commerce) refers to the buying and selling of goods and services over the internet. This web application simulates a real online store where users can:

- **Browse products** across different categories (Electronics, Clothing, Home Appliances)
- **Add items to shopping cart** with dynamic price calculations
- **Apply additional services** like gift wrapping, express shipping, and personalization
- **Purchase product bundles** as complete sets
- **Process payments** through multiple providers
- **Schedule deliveries** with various shipping services

## 🏗️ Structural Design Patterns Implemented

### 1. **Adapter Pattern**
- **Purpose**: Integrate external services with incompatible APIs
- **Implementation**: 
  - Payment services (Stripe, PayPal) with different interfaces
  - Delivery services (DHL, FedEx) with varying data formats
- **Files**: `adapters.py`

### 2. **Decorator Pattern**
- **Purpose**: Dynamically add features to products without modifying their structure
- **Implementation**:
  - Additional services: Gift Wrap, Express Shipping, Personalization, Insurance
  - Real-time price updates when services are selected
- **Files**: `decorators.py`

### 3. **Composite Pattern**
- **Purpose**: Treat individual products and product bundles uniformly
- **Implementation**:
  - Create ready-made bundles (Gaming Computer Bundle, Office Workspace, etc.)
  - Calculate total prices for bundles as single entities
- **Files**: `composite.py`

## 🚀 Features

- **Product Catalog** with categories and search functionality
- **Shopping Cart** with quantity management
- **Dynamic Pricing** with decorator pattern
- **Product Bundles** using composite pattern
- **Payment Processing** via multiple adapters
- **Order Management** with status tracking
- **Responsive UI** with modern design

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Architecture**: REST API with structural design patterns

## 📁 Project Structure
<img width="422" height="586" alt="image" src="https://github.com/user-attachments/assets/d2256d2d-e8ec-411d-a844-8b2fcba5bc2c" />

## 🎯 Educational Value

This project serves as a practical example of how structural design patterns can be applied in real-world e-commerce applications to create:

- **Scalable architecture** that can easily integrate new services
- **Maintainable code** with clear separation of concerns
- **Flexible functionality** that can be extended without breaking existing code
- **Professional software design** following industry best practices

Perfect for understanding how design patterns solve common software architecture problems in commercial web applications!
