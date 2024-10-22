def validate_non_empty_string(value: str, variable_name: str) -> str:
    if not value:
        raise ValueError(f"'{variable_name}' must be a non-empty string.")
    if not isinstance(value, str):
        raise TypeError(
            f"'{variable_name}' should have been a 'str', but was '{type(variable_name)}'."
        )
    if not value.strip():
        raise ValueError(f"'{variable_name}' must be a non-empty string.")
    return value
