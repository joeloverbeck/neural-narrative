import tiktoken


class TokenizeAlgorithm:
    def __init__(self, text: str):
        self._text = text

    def do_algorithm(self) -> int:
        token_count = 0
        if self._text:
            encoding = tiktoken.encoding_for_model("gpt-4")
            tokens = encoding.encode(self._text)
            token_count = len(tokens)

        return token_count
