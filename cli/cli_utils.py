import getpass

class CancelOperation(Exception):
    pass

class QuitProgram(SystemExit):
    pass

def prompt(prompt_text: str, allow_empty: bool = False, validator=None):
    val = input(prompt_text)
    if val.strip().lower() == 'q':
        raise QuitProgram()
    if val.strip().lower() == 'x':
        raise CancelOperation()
    if not allow_empty and val == '':
        return prompt(prompt_text, allow_empty, validator)
    if validator and not validator(val):
        print("Invalid input. Try again.")
        return prompt(prompt_text, allow_empty, validator)
    return val

def secret_prompt(prompt_text: str):
    val = getpass.getpass(prompt_text)
    if val.strip().lower() == 'q':
        raise QuitProgram()
    if val.strip().lower() == 'x':
        raise CancelOperation()
    return val

def confirm(prompt_text: str = "Are you sure? (y/n): ") -> bool:
    val = input(prompt_text).strip().lower()
    if val == 'q':
        raise QuitProgram()
    if val == 'x':
        raise CancelOperation()
    return val in ['y', 'yes']
