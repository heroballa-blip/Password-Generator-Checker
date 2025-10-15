# Password Manager Tools

A simple password password manager tool that uses a password generator and checker built with **Python** and **PyQt5**.
The Password manager is built with **python** and a few **sql** statements here and there and connects to databases via **postgresql**.
This project allows users to generate secure passwords, check their strength, and check them with a password dictionary.

## Project Goal

The goal of this project is to build a **hybrid quantum-resistant password manager** that utilizes existing infrastructure to maximize security against advanced decryption tools Quantum Computing can present.
This includes:
- Integrating **Quantum Random Number Generators (QRNG)** for high-entropy password generation.
- Enforcing **strong password policies** to reduce the risk of brute-force and dictionary attacks.
- Designing a **secure and user-friendly interface** for password management.
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
- pscopg2 for PostgreSQL implementation(currently on CLI)
- QRNG (planned integration)

## Features

- Generate secure passwords with customizable settings
- Real-time strength checking using entropy (weak, medium, strong)
- Optional dictionary check to avoid weak words (penalizes password for each word used)
- Clean and simple GUI built with PyQt5
- Fast and lightweight
- Add Password Database using Postgresql & apply basic encryption logic
- Provide User option to add multiple vaults within database 
- Uses Master Password protection to each vault within

---

## Installation Instructions

```bash
git clone https://github.com/heroballa-blip/Password-Generator-Checker.git
cd Password-Generator-Checker

# (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# OR
.venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
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

- bcrypt==5.0.0
- cryptography==46.0.2
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
- Implement a Master Password with 2FA system to enhance database protection
- Update crypto_utils file to use Argon2 (modern standard), and replace outdated Hashing algorithm (SHA-256)

---

## License

This project is licensed under the MIT License.