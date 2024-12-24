# augmentation\augment_text.py

import random
import re
from typing import Tuple, Optional

import tiktoken
from pydantic import BaseModel


class TextAugmentation(BaseModel):
    seed: int
    word_scrambling: bool
    random_capitalization: bool
    ascii_perturbation: bool
    random_prefix_length: int = 0
    random_suffix_length: int = 0

    def __str__(self):
        return f"seed={self.seed}, RandomCap: {self.random_capitalization}, ASCIIPerturb: {self.ascii_perturbation}, WordScramble: {self.word_scrambling}, PrefixLength: {self.random_prefix_length}, SuffixLength: {self.random_suffix_length}"

    def file_name(self):
        return f"seed={self.seed}_randcap={self.random_capitalization}_asciiperturb={self.ascii_perturbation}_wordscramble={self.word_scrambling}_prefix={self.random_prefix_length}_suffix={self.random_suffix_length}"

    def to_dict(self):
        return {
            "seed": self.seed,
            "random_capitalization": self.random_capitalization,
            "ascii_perturbation": self.ascii_perturbation,
            "word_scrambling": self.word_scrambling,
            "random_prefix_length": self.random_prefix_length,
            "random_suffix_length": self.random_suffix_length,
        }


class AttackString(BaseModel):
    token_ids: list[int]

    def decode(self, tokenizer: tiktoken.core.Encoding) -> str:
        return tokenizer.decode(self.token_ids)

    def get_normalised_string(self, tokenizer: tiktoken.core.Encoding) -> str:
        return " ".join(self.decode(tokenizer).split())


def get_tokenizer() -> tiktoken.core.Encoding:
    return tiktoken.get_encoding("cl100k_base")


def get_filtered_token_ids(
    tokenizer: tiktoken.core.Encoding, regex_pattern: Optional[str] = None
) -> list[int]:
    """Get token IDs optionally filtered by a regex pattern.

    Args:
        tokenizer: The tiktoken tokenizer to use
        regex_pattern: Optional regex pattern to filter tokens. If None, returns all valid token IDs.

    Returns:
        List of token IDs matching the filter criteria
    """
    # Special ids such as <|endoftext|> which we want to avoid sampling
    special_ids = {
        tokenizer.encode(t, allowed_special=tokenizer.special_tokens_set)[0]
        for t in tokenizer.special_tokens_set
    }

    # These cause the tokenizer to crash due to pyo3_runtime.PanicException
    error_ids = set(range(100261, 100276)) | {100256}

    # 0 is our initialisation so we want to avoid that
    disallowed = special_ids | error_ids | {0}
    ids_to_sample = set(range(tokenizer.n_vocab)) - disallowed

    tokens = [
        (identifier, tokenizer.decode([identifier])) for identifier in ids_to_sample
    ]

    if regex_pattern is None:
        return [identifier for identifier, _ in tokens]

    return [
        identifier for identifier, token in tokens if re.match(regex_pattern, token)
    ]


def get_attack_string(num_tokens: int) -> AttackString:
    tokenizer = get_tokenizer()
    all_ids = get_filtered_token_ids(tokenizer)
    attack_string = AttackString(token_ids=random.sample(all_ids, num_tokens))
    return attack_string


def apply_word_scrambling(text: str, sigma: float) -> str:
    """
    Scrambles the middle characters of words longer than 3 characters in the input text.
    The probability of scrambling is determined by sigma.

    Example:
    Input: "The quick brown fox jumps"
    Output: "The qiuck bwron fox jpums"
    """
    words = text.split()
    scrambled_words = []
    for word in words:
        if len(word) > 3 and random.random() < sigma ** (1 / 2):
            chars = list(word)
            middle_chars = chars[1:-1]
            random.shuffle(middle_chars)
            scrambled_word = chars[0] + "".join(middle_chars) + chars[-1]
            scrambled_words.append(scrambled_word)
        else:
            scrambled_words.append(word)
    return " ".join(scrambled_words)


def apply_random_capitalization(text: str, sigma: float) -> str:
    """
    Randomly capitalizes letters in the input text.

    Input: "The quick brown fox jumps"
    Output: "The qUick bRoWn fOx jUmps"
    """
    new_text = []
    for c in text:
        if c.isalpha() and random.random() < sigma ** (1 / 2):
            if "a" <= c <= "z":
                new_text.append(chr(ord(c) - 32))  # Convert to uppercase
            elif "A" <= c <= "Z":
                new_text.append(chr(ord(c) + 32))  # Convert to lowercase
        else:
            new_text.append(c)
    return "".join(new_text)


def apply_ascii_noising(text: str, sigma: float) -> str:
    """
    Perturbs the ASCII characters of the input text.

    Example:
    Input: "The quick brown fox jumps"
    Output: "Tge quick brown fox junps"
    """
    new_text = []
    for c in text:
        if c.isprintable() and random.random() < sigma**3:
            perturbation = random.choice([-1, 1])
            new_char_code = ord(c) + perturbation
            # Ensure new character is printable ASCII
            if 32 <= new_char_code <= 126:
                new_text.append(chr(new_char_code))
            else:
                new_text.append(c)
        else:
            new_text.append(c)
    return "".join(new_text)


def augment_text(
    text: str,
    sigma: float,
    seed: int,
    word_scrambling: bool,
    random_capitalization: bool,
    ascii_perturbation: bool,
    random_prefix_length: int = 0,
    random_suffix_length: int = 0,
) -> Tuple[str, TextAugmentation]:
    if seed is not None:
        random.seed(seed)

    text_augmentation = TextAugmentation(
        seed=seed,
        word_scrambling=word_scrambling,
        random_capitalization=random_capitalization,
        ascii_perturbation=ascii_perturbation,
        random_prefix_length=random_prefix_length,
        random_suffix_length=random_suffix_length,
    )

    # Apply augmentations
    if random_prefix_length > 0:
        prefix = get_attack_string(num_tokens=random_prefix_length)
        text = prefix.get_normalised_string(get_tokenizer()) + "\n\n" + text
    if random_suffix_length > 0:
        suffix = get_attack_string(num_tokens=random_suffix_length)
        text = text + "\n\n" + suffix.get_normalised_string(get_tokenizer())
    if word_scrambling:
        text = apply_word_scrambling(text, sigma)
    if random_capitalization:
        text = apply_random_capitalization(text, sigma)
    if ascii_perturbation:
        text = apply_ascii_noising(text, sigma)

    return text, text_augmentation
