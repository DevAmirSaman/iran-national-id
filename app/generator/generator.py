import random
from typing import Tuple, Optional, List

from app.city_codes.city_codes import random_city_code, get_codes_for_city


def generate_national_id(
        city_code_prefixes: Optional[Tuple[str]] = None,
        quantity: int = 1
) -> List[str]:
    if city_code_prefixes is not None and not isinstance(city_code_prefixes, tuple):
        raise TypeError(f'city_code_prefixes must be a tuple, got {type(city_code_prefixes).__name__}')

    if not 1 <= quantity <= 1000:
        raise ValueError(f'quantity must be between 1 and 1000, got {quantity}')

    use_random_code = not city_code_prefixes
    ids = []
    for _ in range(quantity):
        prefix = random_city_code() if use_random_code else random.choice(city_code_prefixes)
        if not isinstance(prefix, str) or len(prefix) != 3 or not prefix.isdigit():
            continue

        national_id = prefix + ''.join([str(random.randint(0, 9)) for _ in range(6)])

        checksum = 0
        for ch, weight in zip(national_id, range(10, 1, -1)):
            checksum += int(ch) * weight

        check_digit = checksum % 11
        control_digit = check_digit if check_digit < 2 else 11 - check_digit

        ids.append(national_id + str(control_digit))

    return ids
