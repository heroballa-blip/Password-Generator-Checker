# Function to display vault contents
def display_vault(cur, vault_name, cipher, allow_decrypt=True):
    cur.execute(f"SELECT service, username, password FROM {vault_name};")
    rows = cur.fetchall()

    col_no = 4
    col_service = 20
    col_username = 20
    col_password = 30

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