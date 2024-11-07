# src.filesystem.file_operations.py
import json
import logging
import os
import shutil
from pathlib import Path
from typing import List, Any

logger = logging.getLogger(__name__)


def create_empty_file_if_not_exists(file_path: Path) -> None:
    """Create an empty file if it does not exist."""
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8"):
            pass


def create_empty_json_file_if_not_exists(file_path: Path):
    if not os.path.exists(file_path):
        write_json_file(file_path, {})


def create_directories(dir_path: Path) -> None:
    dir_path.mkdir(parents=True, exist_ok=True)


def copy_file(origin_file_path: Path, destination_file_path: Path) -> None:
    shutil.copy(origin_file_path, destination_file_path)


def remove_file(file_path: Path) -> None:
    try:
        os.remove(file_path)
    except Exception as e:
        logger.error("Failed to delete file at '%s': %S", file_path, str(e))
        raise


def remove_folder(folder_path: Path) -> None:
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            logger.info(f"Deleted folder at: {folder_path}")
        except Exception as e:
            logger.error(f"Failed to delete folder at {folder_path}: {e}")
            raise
    else:
        logger.warning(f"Folder does not exist at: {folder_path}")


def read_file_if_exists(file_path: Path) -> str:
    file_contents = ""
    if os.path.exists(file_path):
        file = read_file(file_path)
        if file:
            file_contents = file
    return file_contents


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


def write_binary_file(file_path: Path, contents: bytes) -> None:
    """Write binary contents to a file."""
    with open(file_path, "wb") as f:
        f.write(contents)
