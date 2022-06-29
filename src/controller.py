from random import choice
from string import ascii_letters, digits

def generate_api_key(current_keys):
    api_key = []

    while len(api_key) < 40:
        api_key.append(choice(ascii_letters + digits))

    api_key = "".join(api_key)

    if api_key in current_keys:
        generate_api_key(current_keys)
    else:
        return api_key