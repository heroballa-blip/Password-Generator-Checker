# Password Manager Tools

A simple **password manager** tool that uses a password generator and checker built with **Python** and **PyQt5**.
The password manager connects to databases using a few SQL statements and integrates with **PostgreSQL**.
This project allows users to generate secure passwords, check their strength, and validate them against a dictionary to detect weak patterns.

## Project Goal

The goal of this project is to build a **hybrid quantum-resistant password manager** that uses existing infrastructure to maximize security against advanced decryption tools Quantum Computing can present.
This includes:
- Integrating **Quantum Random Number Generators (QRNG)** for high-entropy password generation.
- Enforcing **strong password policies** to reduce the risk of brute-force and dictionary attacks.
- A **secure and user-friendly interface** for password management.
- Laying the foundation for **future cryptographic integrations**, such as post-quantum encryption.

---

## Project Structure

```
Password-Generator-Checker/
│
├── Resources/
│   └── dictionary.txt
│
├── cli/
│   ├── cli_utils.py
│   ├── crypto_utils.py
│   ├── db_main.py
│   ├── logging_utils.py
│   ├── main_cli.py
|   ├── password_checker.py
|   ├── password_generator.py
|   └── vault_actions.py
|
├── gui/
│   ├── tabs/
│   │   ├── indevelopment_tab.py
│   │   └── password_tab.py
│   ├── utils/
│   │   ├── dictionary_utils.py
│   │   ├── entropy_utils.py
│   │   └── generation_utils.py
│   ├── app_window.py
│   └── main_gui.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Tech Stack
- Python (3.9+)
- PyQt5 for GUI
- Cryptography library for security features
- Imported Psycopg2 for PostgreSQL implementation (currently on CLI version)
- QRNG (planned integration)

## Features

- Generate secure passwords with customizable settings
- Real-time strength checking using entropy (weak, medium, strong)
- Optional dictionary check to avoid weak words (penalizes password for each word used)
- Clean and simple GUI built with PyQt5
- Fast and lightweight
- Add Password Database using Postgresql & apply basic encryption logic
- Provide User option to add multiple vaults within database 
- Uses Master Password protection for accessing database and vault
- Uses Argon2, a modern password hashing librar,y to that help encrypt password

---

## Installation Instructions
---

## 🛠️ Installation Guide

### 1. 📋 Prerequisites

Before you install the project, make sure you have:

- 🐍 **Python 3.10+**
- 🐘 **PostgreSQL** installed and running
- A PostgreSQL user and database set up

---

### 2. 🐘 Install PostgreSQL

#### macOS
```bash
brew install postgresql
brew services start postgresql
```

#### Ubuntu / Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Windows
Download and install from [https://www.postgresql.org/download/](https://www.postgresql.org/download/)  
Make sure `psql` is added to your PATH during installation.

---

### 3. 🧰 Database Setup

Once PostgreSQL is installed, create a database and user:

```bash
# Enter the PostgreSQL shell
psql postgres

# Inside psql:
CREATE DATABASE vault_db;
CREATE USER vault_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE vault_db TO vault_user;
\q
```

> 📝 **Note:** You can customize the database name, user, and password — just make sure to update your config or `.env` accordingly.

---

### 4. Install Python Dependencies

It's recommended to use a virtual environment to help organize libaries:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```



---

### 5. Configure Environment Variables

Create a `.env` file in the root directory with:

```
DB_NAME=vault_db
DB_USER=vault_user
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```

---

### 6. Run the Application

Run the **GUI version**:
```bash
python gui/main_gui.py
```

Run the **CLI version**:
```bash
python cli/main_cli.py
```

---

## Usage

```bash
# Run GUI
python gui/main_gui.py

# Run CLI version
python cli/main_cli.py
```

---

## Dependencies

- argon2-cffi==25.1.0
- cryptography==46.0.2
- psycopg2==2.9.11
- pyperclip==1.11.0
- PyQt5==5.15.11
- PyQt5-Qt5==5.15.17
- PyQt5_sip==12.17.1

---

## Future Plans for Project

- Integrate QRNG for enhanced randomness
- Implement a feature to export generated passwords to a encrypted text file
- Improve UI design and add dark mode
- Implement a web version of this project
- Connect CLI - GUI - WEB to a encrypted Postgresql database
- Implement 2FA system to further enhance security

---

## License

This project is licensed under the MIT License.