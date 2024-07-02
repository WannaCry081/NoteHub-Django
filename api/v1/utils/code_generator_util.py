import random
from string import digits, ascii_letters


def code_generator(length: int = 8) -> str:
    symbols = digits + ascii_letters
    return "".join([random.choice(symbols) for i in range(0, length)])
