# 📦 Inventory Management System (DBMS)

A **database-driven Inventory Management System** for managing products, suppliers, stock levels, and transactions.  
Includes a relational database schema, SQL queries, and a user-friendly GUI built with `tkinter`.

---

## 🚀 Features

- Manage products, suppliers, and warehouses
- Track stock entries and inventory levels
- View historical inventory changes
- GUI interface with `tkinter`
- MySQL database integration

---

## 🛠️ Technologies Used

- Python 3.x  
- MySQL  
- tkinter (built-in GUI library)  
- mysql-connector-python  

---

## ⚙️ Setup Instructions

### 1. 📥 Clone the repository
```bash
git clone https://github.com/quanninja1304/inventory-management-system-dbms.git
cd inventory-management-system-dbms  
```
### 2. 🧪 Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Set up the MySQL database
- Ensure MySQL is running locally

- Create the necessary database and tables (use `database.sql` if provided)

- Update your `database.py` with the correct connection credentials
---
## 📁 Project Structure
```
inventory-management-system-dbms/  
├── app/
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── controller.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── sql/
│   │   └── sql_script.sql
│   └── views/
│       ├── __init__.py
│       └── view.py
├── .env               # Store actual credentials here
├── .env.example       # Template with placeholders
├── .gitignore         # Make sure .env is listed here
├── config.py          # Load config from .env
├── inventory_system.log
├── main.py            # Entry point
├── README.md
└── requirements.txt