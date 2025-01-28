"""
Simple local parser for gathering all music files in xls table
"""

import logging
from typing import Final
from pathlib import Path

from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(module)s %(levelname)s %(message)s"
)


def get_files_from_directory(path: Path) -> set:
    """
    Colllects recursively all music files and returns
    deducpicated set of them
    """
    files = set()
    for file in tqdm(
        path.rglob("*"),
        desc="Collecting files",
    ):
        if file.suffix in MUSIC_FORMATS:
            files.add(file)
    return files


def process_mp3() -> None:
    """Process .mp3 files and get tags"""
    pass


def process_wav() -> None:
    """Process .wav files"""
    pass


def process_flac() -> None:
    """Process .flac files and get tags"""
    pass


def process_ogg() -> None:
    """Process .ogg files and get tags"""
    pass


def main(path: Path, file: Path) -> None:
    """Main function that initiate parsing"""
    files = get_files_from_directory(path=path)
    with file.open() as document:
        document.write_text(files)



if __name__ == "__main__":
    MUSIC_FORMATS: Final = frozenset([".mp3", ".wav", ".flac", ".ogg", ".m4a"])
    COLLECTION_DIR_PATH: Final = Path(__file__).parent.joinpath("catalog")
    COLLECTION_FILE_PATH: Final = Path(__file__).parent.joinpath(
        COLLECTION_DIR_PATH, "collection.xls"
    )

    while True:
        directory = Path(str(input("Enter directory to parse: ")))
        if directory.exists():
            break

        logging.error("No such directory")

    if not COLLECTION_DIR_PATH.exists():
        COLLECTION_DIR_PATH.mkdir()
        COLLECTION_FILE_PATH.touch()

    main(path=directory, file=COLLECTION_FILE_PATH)
