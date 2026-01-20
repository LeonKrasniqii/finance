from pydantic import validator

def validate_positive(value: float) -> float:
    if value <= 0:
        raise ValueError("Must be positive")
    return value
