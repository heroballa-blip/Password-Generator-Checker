import getpass
from logging_utils import log_edit, log_access
from crypto_utils import derive_key
from cryptography.fernet import Fernet, InvalidToken


def insert_password(cur, conn, username, vault_name, cipher, password=None, vault_success=True):
    if not vault_success:
        print("Cannot insert: wrong vault key.")
        return

    service = input("Service name: ")
    account_user = input("Account username: ")

    plain_pw = password if password is not None else getpass.getpass("Account password: ")
    encrypted_pw = cipher.encrypt(plain_pw.encode()).decode()

    cur.execute(f"""
        INSERT INTO {vault_name} (service, username, password)
        VALUES (%s, %s, %s);
    """, (service, account_user, encrypted_pw))
    conn.commit()

    print(f"Password for {service} added to {vault_name}")
    log_edit(username, vault_name, service, "INSERT")
    display_vault(cur, vault_name, cipher)


def update_password(cur, conn, username, vault_name, cipher, vault_success):
    if not vault_success:
        print("Cannot update: wrong vault key.")
        return

    display_vault(cur, vault_name, cipher)
    row_no = input("\nEnter the No. of the service you want to update: ").strip()
    if not row_no.isdigit():
        print("Invalid input.")
        return
    row_idx = int(row_no) - 1

    cur.execute(f"SELECT service, username, password FROM {vault_name};")
    rows = cur.fetchall()
    if row_idx < 0 or row_idx >= len(rows):
        print("Invalid service number.")
        return

    old_service, old_username, old_password_encrypted = rows[row_idx]

    new_service = input(f"New service name (leave blank to keep '{old_service}'): ").strip() or old_service
    new_username = input(f"New account username (leave blank to keep '{old_username}'): ").strip() or old_username
    new_password = getpass.getpass("New account password (leave blank to keep current): ").strip()

    encrypted_pw = cipher.encrypt(new_password.encode()).decode() if new_password else old_password_encrypted

    cur.execute(f"""
        UPDATE {vault_name}
        SET service=%s, username=%s, password=%s
        WHERE service=%s;
    """, (new_service, new_username, encrypted_pw, old_service))
    conn.commit()

    print(f"Updated service '{old_service}' to '{new_service}' in '{vault_name}'")
    log_edit(username, vault_name, new_service, "UPDATE")
    display_vault(cur, vault_name, cipher)


def delete_password(cur, conn, username, vault_name, cipher, vault_success):
    if not vault_success:
        print("Cannot delete: wrong vault key.")
        return

    display_vault(cur, vault_name, cipher)
    row_no = input("\nEnter the No. of the service you want to delete: ").strip()
    if not row_no.isdigit():
        print("Invalid input.")
        return
    row_idx = int(row_no) - 1

    cur.execute(f"SELECT service FROM {vault_name};")
    rows = cur.fetchall()
    if row_idx < 0 or row_idx >= len(rows):
        print("Invalid service number.")
        return

    service = rows[row_idx][0]
    cur.execute(f"DELETE FROM {vault_name} WHERE service=%s;", (service,))
    conn.commit()
    print(f"Password for {service} deleted from {vault_name}")
    log_edit(username, vault_name, service, "DELETE")
    display_vault(cur, vault_name, cipher)


def create_vault(cur, conn, username):
    vault_name = input("Enter a name for the new vault: ").strip()
    if not vault_name:
        print("Vault name cannot be empty.")
        return

    # Prompt for vault password
    while True:
        vault_password = getpass.getpass("Create a password to encrypt this vault (required): ").strip()
        if not vault_password:
            print("Password cannot be empty. Please try again.")
            continue
        confirm_pw = getpass.getpass("Confirm vault password: ").strip()
        if vault_password != confirm_pw:
            print("Passwords do not match. Try again.")
        else:
            break

    # Derive encryption key and salt
    vault_key, salt = derive_key(vault_password)
    cipher = Fernet(vault_key)

    # Store salt in vault_salts table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vault_salts (
            vault_name TEXT PRIMARY KEY,
            salt BYTEA NOT NULL
        );
    """)
    cur.execute("INSERT INTO vault_salts (vault_name, salt) VALUES (%s, %s);", (vault_name, salt))

    # Create vault table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {vault_name} (
            id SERIAL PRIMARY KEY,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    print(f"Vault '{vault_name}' created successfully.")
    log_access(username, "CREATE VAULT", vault_name)

    if input("Do you want to add a password now? [y/n]: ").strip().lower() == 'y':
        insert_password(cur, conn, username, vault_name, cipher, vault_success=True)


def delete_vault(cur, conn, username):
    # List vaults
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema='public';
    """)
    tables = [t[0] for t in cur.fetchall()]
    if not tables:
        print("No vaults to delete.")
        return

    print("\nExisting vaults:")
    for idx, t in enumerate(tables, start=1):
        print(f"{idx}. {t}")

    vault_input = input("Enter the vault name or ID to delete: ").strip()
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

    # Confirm deletion
    confirm_pw = getpass.getpass(f"Enter the password to confirm deletion of vault '{vault_name}': ").strip()
    if not confirm_pw:
        print("Vault deletion cancelled (no password entered).")
        return

    # Retrieve stored salt
    cur.execute("SELECT salt FROM vault_salts WHERE vault_name=%s;", (vault_name,))
    row = cur.fetchone()
    if not row:
        print("Salt not found. Cannot delete vault securely.")
        return
    salt = row[0]

    # Derive key and validate
    vault_key, _ = derive_key(confirm_pw, salt)
    cipher = Fernet(vault_key)
    try:
        cur.execute(f"SELECT password FROM {vault_name} LIMIT 1;")
        row = cur.fetchone()
        if row:
            cipher.decrypt(row[0].encode())  # Verify password
    except (InvalidToken, TypeError):
        print("Wrong password! Vault not deleted.")
        return

    # Delete vault and salt
    cur.execute(f"DROP TABLE IF EXISTS {vault_name};")
    cur.execute("DELETE FROM vault_salts WHERE vault_name=%s;", (vault_name,))
    conn.commit()

    print(f"Vault '{vault_name}' has been deleted.")
    log_access(username, "DELETE VAULT", vault_name)


def display_vault(cur, vault_name, cipher, allow_decrypt=True):
    cur.execute(f"SELECT service, username, password FROM {vault_name};")
    rows = cur.fetchall()

    col_no, col_service, col_username, col_password = 4, 20, 20, 30
    print(f"\n{'No.'.ljust(col_no)} | {'Service'.ljust(col_service)} | {'Username'.ljust(col_username)} | {'Password'.ljust(col_password)}")
    print("-" * (col_no + col_service + col_username + col_password + 9))

    for idx, (s, u, p) in enumerate(rows, start=1):
        if allow_decrypt:
            try:
                decrypted_pw = cipher.decrypt(p.encode()).decode()
                pw_display = decrypted_pw
            except Exception:
                pw_display = "Cannot decrypt"
        else:
            pw_display = "Cannot decrypt"
        print(f"{str(idx).ljust(col_no)} | {s.ljust(col_service)} | {u.ljust(col_username)} | {pw_display.ljust(col_password)}")
