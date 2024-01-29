import random
LENGHT = 6
CHARACTERS = 'ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz234567890'  # алфавит для генерации короткой ссылки

def generate_short_url():
    short_url = ''.join(random.choices(CHARACTERS, k=LENGHT))
    return short_url