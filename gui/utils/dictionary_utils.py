import os

def get_dictionary_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))
    return os.path.join(root_dir, "resources", "dictionary.txt")

def load_dictionary():
    path = get_dictionary_path()
    if not os.path.exists(path):
        print(f"Dictionary file not found at: {path}")
        return set()
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return {line.strip().lower() for line in f if len(line.strip()) >= 3}
