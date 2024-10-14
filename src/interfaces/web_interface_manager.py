class WebInterfaceManager:
    @staticmethod
    def remove_excessive_newline_characters(text: str):
        return text.replace("\r\n", "\n").strip()
