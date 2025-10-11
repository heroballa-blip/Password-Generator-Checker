# Password Generator & Strength Checker

A simple yet powerful password generator and strength checker built with **Python** and **PyQt5**.
This project allows users to generate secure passwords, check their strength, and optionally validate them against a custom dictionary.

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
│   ├── main_cli.py
│   ├── password_checker.py
│   └── password_generator.py
│
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
- PostgreSQL (planned)
- QRNG (planned integration)

## Features

- Generate secure passwords with customizable settings
- Real-time strength checking using entropy (weak, medium, strong)
- Optional dictionary check to avoid weak words (penalizes password for each word used)
- Clean and simple GUI built with PyQt5
- Fast and lightweight

---

## Installation

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

- Python 3.9+
- PyQt5
- cryptography
- Rest of the dependencies are listed in `requirements.txt`

---

## Future Plans for Project

- [ ] Add Password Database using Postgresql & apply basic encryption logic
- [ ] Integrate QRNG for enhanced randomness
- [ ] Export generated passwords to a encrypted text file
- [ ] Improve UI design and add dark mode
- [ ] Implement a web version of this project
- [ ] Connect CLI - GUI - WEB to a encrypted Postgresql database
- [ ] Implement a Master Password with 2FA system to enhance database protection
- [ ] Provide User option to add multiple vaults within database and implement Master Password protection to each vault within

---

## License

This project is licensed under the MIT License.