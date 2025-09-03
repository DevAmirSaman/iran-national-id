def is_national_id_valid(national_id: str) -> bool:
    if len(national_id) != 10 or not national_id.isdigit():
        return False

    checksum = 0
    for ch, weight in zip(national_id[:9], range(10, 1, -1)):
        checksum += int(ch) * weight

    check_digit = checksum % 11
    return int(national_id[9]) == (check_digit if check_digit < 2 else 11 - check_digit)
