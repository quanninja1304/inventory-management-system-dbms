# 📦 Inventory Management System (DBMS)

A **database-driven Inventory Management System** for managing products, suppliers, warehouses, and stock transactions.  
Features a relational MySQL database and a user-friendly GUI built with `tkinter`.

---

## 🚀 Features
- Manage products, suppliers, and warehouses
- Track inventory levels and stock entries
- Generate reports (low stock, stock value, transaction history)
- GUI interface with `tkinter`
- MySQL database integration

---

## 🛠️ Prerequisites
- Python 3.8+
- MySQL Server
- MySQL Workbench (optional)
- pip (Python package manager)
- Python 3.8 or higher
- MySQL Server
- `tkinter` (comes with Python on Windows/macOS)

  - If you're on Linux, install with:
    ```bash
    sudo apt-get install python3-tk
    ```

---

## ⚙️ Setup Instructions

### 🗄️ Database Setup

1. **Create MySQL Database**  
   Run the SQL script to set up the database schema and default data:

   ```bash
   mysql -u root -p < app/sql/sql_script.sql
2. **Verify Database Connection**  
   Log into MySQL and connect directly to the newly created database:

   ```bash
   mysql -u root -p inventory_db
### 🖥️ Application Setup

1. **Clone the Repository**

   Use the following commands to download and enter the project folder:

   ```bash
   git clone https://github.com/quanninja1304/inventory-management-system-dbms.git
   cd inventory-management-system-dbms
2. **Set Up Virtual Environment**:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    source venv/bin/activate  # Linux/Mac
    ```
3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Configure Environment**:
- Copy `.env.example` to `.env`

- Update database credentials in `.env`
5. **Run Application**:
    ```bash
    python main.py
    ```

---
## 📁 Project Structure
```
inventory-management-system-dbms/
├── controllers/                 # Business logic
│   ├── __init__.py
│   └── controller.py            # Coordinates between model and view
├── database/                    # DB connection
│   ├── __init__.py
│   └── database.py              # Connects to MySQL using .env
├── models/                      # Data models
│   ├── __init__.py
│   └── models.py                # Product, supplier, inventory models
├── views/                       # GUI components
│   ├── __init__.py
│   └── view.py                  # tkinter UI layout
├── sql/                         # SQL setup
│   └── sql_script.sql           # DB schema and initial data
├── .env                         # Environment variables (gitignored)
├── config.py                    # Loads config from .env
├── main.py                      # App entry point
├── README.md                    # Project documentation
└── requirements.txt             # Python dependencies
```
---
## ⚠️ Important Notes

- **Update default database credentials** in your `.env` file before running the app:

  ```env
  DB_HOST=localhost
  DB_USER=root
  DB_PASSWORD=your_password
  DB_NAME=inventory_db
  ```
- ✅ All sensitive files (like `.env`) are excluded from version control via `.gitignore`   .
## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
