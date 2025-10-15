import getpass
from cryptography.fernet import Fernet
from password_generator import prompt_length, exclude_special_char, generate_password
from password_checker import checker, calculate_entropy, strength_rating
from cli_utils import prompt, CancelOperation, QuitProgram


import db_main as db_main
from vault_actions import insert_password, create_vault


# Helps to save a generated or checked password to a vault
def save_to_vault_option(username, conn, cur, password):
    """
    Saves a password to an existing vault (caller already confirmed 'y').
    """
    # List vaults in current DB
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = [t[0] for t in cur.fetchall()]
    if not tables:
        print("No vaults found. You need to create one first.")
        create_vault(cur, conn, username)
        return

    print("\nExisting vaults:")
    for idx, t in enumerate(tables, start=1):
        print(f"{idx}. {t}")

    vault_input = input("Enter vault name or ID to save the password: ").strip()
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

    # Vault decryption password
    vault_password = getpass.getpass("Enter vault decryption password: ")
    vault_key = db_main.derive_key(vault_password)
    cipher = Fernet(vault_key)

    insert_password(cur, conn, username, vault_name, cipher, password)


# Main CLI menu for password tools and vault access
def password_tools_menu():
    """
    Main CLI menu for password tools and vault access.
    """
    while True:
        try:
            menu = prompt(
                "Choose a tool below:\n"
                " (1) Password Generator\n"
                " (2) Password Checker\n"
                " (3) Vault (PostgreSQL)\n"
                " Exit? (x/q)\n=> "
            ).lower()
        except (CancelOperation, QuitProgram):
            print("Exiting Tool")
            return

        if menu == "1":
            # Password Generator
            while True:
                try:
                    length = prompt_length()
                    exclude = exclude_special_char()
                    pwd = generate_password(length, exclude)
                    entropy = calculate_entropy(length, exclude)
                    print(f"\nGenerated Password: {pwd}")
                    print(f"Entropy: {entropy} bits")
                    print(f"Strength: {strength_rating(entropy)}")
                    print("-" * 40)

                    # Optionally save to vault
                    save_now = prompt("Do you want to save this password to a vault? (y/n): ").lower()
                    if save_now == "y":
                        username, conn, cur = db_main.login()
                        if username:
                            save_to_vault_option(username, conn, cur, pwd)
                            # Close connection after finished saving
                            if cur:
                                cur.close()
                            if conn:
                                conn.close()


                    again = prompt("Generate another password? (y/n): ").lower()
                    if again != "y":
                        break
                except (CancelOperation, QuitProgram):
                    return

        elif menu == "2":
    # Password Checker
            while True:
                try:
                    pwd_to_check = checker()  # get the password from checker
                    save_now = prompt("Do you want to save this password to a vault? (y/n): ").lower()
                    if save_now == "y":
                        username, conn, cur = db_main.login()
                        if username:
                            save_to_vault_option(username, conn, cur, pwd_to_check)
                            if cur:
                                cur.close()
                            if conn:
                                conn.close()

                    again = prompt("Check another password? (y/n): ").lower()
                    if again != "y":
                        break
                except (CancelOperation, QuitProgram):
                    return

        elif menu == "3":
            # Launch Vault (PostgreSQL) menu
            db_main.main()

        else:
            print("Unknown option — please choose 1, 2, 3 or (x/q) to exit.")


# Execute the main menu
if __name__ == "__main__":
    password_tools_menu()