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

    def get_name(self) -> str:
        return self._name

    def supports_tools(self) -> bool:
        return self._supports_tools
