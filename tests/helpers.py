import random
import string


def get_random_string(n: int):
    chars = string.ascii_letters + string.digits + "_-"
    return "".join(random.choice(chars) for i in range(n))
