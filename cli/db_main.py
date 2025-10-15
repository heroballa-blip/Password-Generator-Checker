import psycopg2
import getpass
from cryptography.fernet import Fernet, InvalidToken
from vault_actions import insert_password, update_password, delete_password, create_vault, delete_vault, display_vault
from logging_utils import log_access
from crypto_utils import derive_key


# login function to connect to an existing database
def login():
    username = input("Enter your database username: ").strip()
    db_password = getpass.getpass("Enter password: ")
    host = input("Enter Postgres host (default localhost): ").strip() or "localhost"
    port = input("Enter Postgres port (default 5432): ").strip() or "5432"
    db_name = input("Enter the database name to connect to: ").strip()

    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=username,
            password=db_password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        print(f"Successfully logged in as {username}")
        log_access(username, "LOGIN")
        return username, conn, cur
    except psycopg2.OperationalError:
        print("Invalid username, password, or database name.")
        log_access(username, "LOGIN", success=False)
        return None, None, None

# Menu to view and manage vaults
def view_vault(username, cur, conn):
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = [t[0] for t in cur.fetchall()]

    if not tables:
        print("No vaults found.")
        return

    print("\nExisting vaults:")
    for idx, t in enumerate(tables, start=1):
        print(f"{idx}. {t}")

    vault_input = input("Enter vault name or ID to access: ").strip()
    if vault_input.isdigit():
        vault_index = int(vault_input) - 1
        if 0 <= vault_index < len(tables):
            vault_name = tables[vault_index]
        else:
            print("Vault ID not found.")
            return
    else:
        if vault_input in tables:
            vault_name = vault_input
        else:
            print("Vault name not found.")
            return

    # --- Argon2 Key Derivation ---
    vault_password = getpass.getpass("Enter vault decryption password: ")

    # Load or generate salt for this vault
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vault_salts (
            vault_name TEXT PRIMARY KEY,
            salt BYTEA NOT NULL
        );
    """)

    cur.execute("SELECT salt FROM vault_salts WHERE vault_name = %s;", (vault_name,))
    row = cur.fetchone()

    if row:
        salt = row[0]
    else:
        # generate and store salt if this is first access
        _, salt = derive_key(vault_password)
        cur.execute("INSERT INTO vault_salts (vault_name, salt) VALUES (%s, %s);", (vault_name, salt))
        conn.commit()

    vault_key, _ = derive_key(vault_password, salt)
    cipher = Fernet(vault_key)

    try:
        cur.execute(f"SELECT password FROM {vault_name} LIMIT 1;")
        row = cur.fetchone()
        if row:
            cipher.decrypt(row[0].encode())
        vault_success = True
    except (InvalidToken, TypeError):
        vault_success = False

    if not vault_success:
        print("Wrong vault key! Vault cannot be accessed or modified.")
        log_access(username, "ACCESS VAULT FAILED", vault_name, success=False)
        return

    display_vault(cur, vault_name, cipher, allow_decrypt=True)
    log_access(username, "ACCESS VAULT", vault_name, success=True)

    while True:
        action = input("\n(1) Insert  (2) Update  (3) Delete  (4) Back: ").strip()
        if action == "1":
            insert_password(cur, conn, username, vault_name, cipher, vault_success)
        elif action == "2":
            update_password(cur, conn, username, vault_name, cipher, vault_success)
        elif action == "3":
            delete_password(cur, conn, username, vault_name, cipher, vault_success)
        elif action == "4":
            break
        else:
            print("Invalid choice")

def vault_menu(username, conn, cur):
    try:
        while True:
            choice = input(
                "\n(1) View existing vaults\n"
                "(2) Create a new vault\n"
                "(3) Delete a vault\n"
                "(4) Exit\n"
                "[1-4]: "
            ).strip()

            if choice == "1":
                view_vault(username, cur, conn)
            elif choice == "2":
                vault_name = create_vault(cur, conn, username)
                if vault_name:
                    print(f"Vault '{vault_name}' created.")
            elif choice == "3":
                delete_vault(cur, conn, username)
            elif choice == "4":
                log_access(username, "LOGOUT")
                print("Logged out.")
                break
            

            else:
                print("Wrong choice, try again.")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Main Menu listing out actions
def main():
    while True:
        print("\n=== Password Vault (PostgreSQL) ===\n"
            "[1] Create new database \n"
            "[2] Access existing database\n"
            "[3] List existing databases\n"
            "[4] Delete database\n"
            "[5] Exit")

        option = input("=> ").strip()

        if option == "1":
            create_database()
        elif option == "2":
            username, conn, cur = login()
            if username:
                vault_menu(username, conn, cur)
        elif option == "3":
             list_databases()
        elif option == "4":
            delete_database()
        elif option == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

# Helps to connect to the Postgres server
def connect_server():
    username = input("Enter your database username: ").strip()
    password = getpass.getpass("Enter password: ")
    host = input("Enter Postgres host (default localhost): ").strip() or "localhost"
    port = input("Enter Postgres port (default 5432): ").strip() or "5432"
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=username,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        print(f"Connected to Postgres server as {username}")
        return conn, username, password, host, port
    except psycopg2.OperationalError as e:
        print("Could not connect to server:", e)
        return None, None, None, None, None

def create_database():
    conn, username, password, host, port = connect_server()
    if not conn:
        return
    cur = conn.cursor()
    db_name = input("Enter name for new database: ").strip()
    try:
        cur.execute(f"CREATE DATABASE {db_name};")
        print(f"Database '{db_name}' created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print("Database already exists.")
    finally:
        cur.close()
        conn.close()

def delete_database():
    conn, username, password, host, port = connect_server()
    if not conn:
        return
    cur = conn.cursor()
    db_name = input("Enter name of database to delete: ").strip()
    confirm = input(f"Are you sure you want to delete '{db_name}'? (y/N): ").strip().lower()
    if confirm == 'y':
        try:
            cur.execute(f"DROP DATABASE {db_name};")
            print(f"Database '{db_name}' deleted.")
        except psycopg2.errors.InvalidCatalogName:
            print("Database does not exist.")
    cur.close()
    conn.close()

#Lists out existing databases
def list_databases():
    conn, username, password, host, port = connect_server()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        dbs = [row[0] for row in cur.fetchall()]
        if not dbs:
            print("No databases found.")
            return
        print("\nExisting databases:")
        for idx, db in enumerate(dbs, start=1):
            print(f"{idx}. {db}")
    except Exception as e:
        print("Error listing databases:", e)
    finally:
        cur.close()
        conn.close()
