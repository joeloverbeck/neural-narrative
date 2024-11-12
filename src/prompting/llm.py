class Llm:
    def __init__(self, model_data: dict):
        # Define the required fields and their expected types
        required_fields = {
            "supports_tools": bool,
            "temperature": float,
            "top_p": float,
            "frequency_penalty": float,
            "presence_penalty": float,
        }

        # Check for the presence of the 'name' key
        name = model_data.get("name")
        if name is None:
            raise ValueError(f"Expected to find key 'name' in model_data: {model_data}")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                f"There wasn't a proper name in the model_data: {model_data}"
            )
        self._name = name

        # Iterate over the required fields to validate and assign them
        for key, expected_type in required_fields.items():
            if key not in model_data:
                raise ValueError(
                    f"Expected to find key '{key}' in model_data: {model_data}"
                )

            value = model_data[key]
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"'{key}' of model_data should have been {expected_type.__name__}, "
                    f"but was '{type(value).__name__}'."
                )

            setattr(self, f"_{key}", value)

    def get_name(self) -> str:
        return self._name

    def get_temperature(self) -> float:
        return self._temperature  # noqa

    def get_top_p(self) -> float:
        return self._top_p  # noqa

    def get_frequency_penalty(self) -> float:
        return self._frequency_penalty  # noqa

    def get_presence_penalty(self) -> float:
        return self._presence_penalty  # noqa

    def supports_tools(self) -> bool:
        return self._supports_tools  # noqa
