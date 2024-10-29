class Llm:
    def __init__(self, model_data: dict):
        if not "name" in model_data:
            raise ValueError(f"Expected to find key 'name' in model_data: {model_data}")

        self._name = model_data["name"]

        if not self._name:
            raise ValueError(
                f"There wasn't a proper name in the model_data: {model_data}"
            )

        if not "supports_tools" in model_data:
            raise ValueError(
                f"Expected to find key 'supports_tools' in model_data: {model_data}"
            )

        self._supports_tools = model_data["supports_tools"]

        if not isinstance(self._supports_tools, bool):
            raise TypeError(
                f"supports_tools of model_data should have been bool, but was '{type(self._supports_tools)}'."
            )

        self._temperature = model_data["temperature"]

        if not isinstance(self._temperature, float):
            raise TypeError(
                f"temperature of model_data should have been float, but was '{type(self._temperature)}'."
            )

        self._top_p = model_data["top_p"]

        if not isinstance(self._top_p, float):
            raise TypeError(
                f"top_p of model_data should have been float, but was '{type(self._top_p)}'."
            )

    def get_name(self) -> str:
        return self._name

    def get_temperature(self) -> float:
        return self._temperature

    def get_top_p(self) -> float:
        return self._top_p

    def supports_tools(self) -> bool:
        return self._supports_tools
