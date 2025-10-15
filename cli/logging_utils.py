import os
import socket
import logging
from logging.handlers import RotatingFileHandler
import psycopg2
from psycopg2 import sql, Error

# Set up logging directory and file paths
LOG_DIR = os.path.join("resources", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

ACCESS_LOG_PATH = os.path.join(LOG_DIR, "access_log.txt")
EDIT_LOG_PATH = os.path.join(LOG_DIR, "edit_log.txt")

# Create a logger, set level, and add rotating file handler
def create_logger(log_path):
    logger = logging.getLogger(log_path)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

access_logger = create_logger(ACCESS_LOG_PATH)
edit_logger = create_logger(EDIT_LOG_PATH)

# Parameters for DB connection
DB_PARAMS = {
    "dbname": "test_db",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

def _get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "UNKNOWN"
    return ip

def _log_to_db(table, username, vault_name, action, status):
    try:
        conn = psycopg2.connect(
            dbname=DB_PARAMS["dbname"],
            user=DB_PARAMS["user"],
            password=DB_PARAMS["password"],
            host=DB_PARAMS["host"],
            port=DB_PARAMS["port"]
        )
        cur = conn.cursor()
        cur.execute(
            sql.SQL("""
                CREATE TABLE IF NOT EXISTS vault_logs (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    vault_name TEXT,
                    action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    ip TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        )
        cur.execute(
            "INSERT INTO vault_logs (username, vault_name, action, status, ip) VALUES (%s, %s, %s, %s, %s)",
            (username, vault_name, action, status, _get_ip())
        )
        conn.commit()
        cur.close()
        conn.close()
    except Error as e:
        access_logger.error(f"DB logging failed: {e}")

# Functions to log access and edits
def log_access(username: str, action: str, vault_name: str = '', success: bool = True):
    status = "SUCCESS" if success else "FAILED"
    # Log to file
    access_logger.info(f"{username} | {vault_name or '-'} | {status} | {action}")
    # Log to DB
    _log_to_db("vault_logs", username, vault_name, action, status)

def log_edit(username: str, vault_name: str, service: str, action: str):
    # Log to file
    edit_logger.info(f"{username} | {vault_name} | {service} | {action}")
    # Log to DB
    _log_to_db("vault_logs", username, vault_name, f"{action} ({service})", "SUCCESS")
