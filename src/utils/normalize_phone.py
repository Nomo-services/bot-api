import phonenumbers

from src.errors.auth import PhoneNumberValidateError


def normalize_phone_number(value: str, region: str = "RU") -> str:
    try:
        parsed = phonenumbers.parse(value, region)
    except phonenumbers.NumberParseException as e:
        raise PhoneNumberValidateError(f"Invalid phone format: {e}") from e

    if not phonenumbers.is_valid_number(parsed):
        raise PhoneNumberValidateError("Phone number is not valid")

    return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
