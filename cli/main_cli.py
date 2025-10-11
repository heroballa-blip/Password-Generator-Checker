from password_generator import (
    prompt_length,
    exclude_special_char,
    generate_password,
)
from password_checker import (
    checker,
    calculate_entropy,
    strength_rating
)
from cli_utils import prompt, CancelOperation, QuitProgram

def main():
    while True:
        try:
            menu = prompt(
                "Choose a tool below:\n"
                " (1) Password Generator\n"
                " (2) Password Checker\n"
                " Exit? (x/q)\n=> "
            ).lower()
        except (CancelOperation, QuitProgram):
            print("Exiting Tool")
            return

        if menu == "1":
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
                    again = prompt("Generate another password? (y/n): ").lower()
                    if again != "y":
                        break
                except (CancelOperation, QuitProgram):
                    return

        elif menu == "2":
            while True:
                try:
                    checker()
                    print("-" * 40)
                    again = prompt("Check another password? (y/n): ").lower()
                    if again != "y":
                        break
                except (CancelOperation, QuitProgram):
                    return

        else:
            print("Unknown option — please choose 1, 2 or (x/q) to exit.")

if __name__ == "__main__":
    main()
