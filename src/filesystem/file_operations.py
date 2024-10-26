# src.filesystem.file_operations.py
import json
from pathlib import Path
from typing import List, Any


def read_file(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8") as file:
        return file.read().strip()


def write_file(file_path: Path, contents: str) -> None:
    with file_path.open("w", encoding="utf-8") as file:
        file.write(contents)


def append_to_file(file_path: Path, contents: str) -> None:
    with file_path.open("a", encoding="utf-8") as file:
        file.write(contents)


def read_json_file(file_path: Path) -> Any:
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json_file(file_path: Path, data: Any) -> None:
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)  # noqa


def read_file_lines(file_path: Path) -> List[str]:
    with file_path.open("r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]
