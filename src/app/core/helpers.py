import string
import random
from hashlib import shake_256
from slugify import slugify


def generate_random_string(length: int) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def slugify_string(my_string: str) -> str:
    random_string = generate_random_string(10)
    return f"{slugify(my_string)}-{shake_256(random_string.encode()).hexdigest(4)}"
