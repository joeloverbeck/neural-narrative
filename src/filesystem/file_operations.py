# src.filesystem.file_operations.py

from pathlib import Path
from typing import List


def read_file(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8") as file:
        return file.read().strip()


def read_file_lines(file_path: Path) -> List[str]:
    with file_path.open("r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]
