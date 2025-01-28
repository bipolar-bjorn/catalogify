"""
Simple local parser for gathering all music files in xls table
"""

import logging
from typing import Final
from pathlib import Path

import pandas as pd
from tqdm import tqdm
from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError

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
        if file.name.startswith("."):
            continue

        if file.suffix in MUSIC_FORMATS:
            files.add(file)
    return files


def process_mp3(file: Path) -> pd.DataFrame:
    """Process .mp3 files and get tags"""
    try:
        track = EasyID3(file)
        tags = {
            "file_path": str(file.absolute()),
            "artist": track.get("artist", [""])[0],
            "album": track.get("album", [""])[0],
            "title": track.get("title", [""])[0],
            "year": track.get("date", [""])[0],
            "genre": track.get("genre", [""])[0],
        }
        return pd.DataFrame([tags])
    except ID3NoHeaderError:
        logging.warning(f"File {file} doesn't start with an ID3 tag and will be skipped.")
        return pd.DataFrame(columns=["file_path", "artist", "album", "title", "year", "genre"])


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
    df = pd.DataFrame(columns=["file_path", "artist", "album", "year", "genre"])
    for file_path in files:
        if file_path.suffix == ".mp3":
            data = process_mp3(file=file_path)
            df = pd.concat([df, data], ignore_index=True)
    df.to_excel(file.with_suffix(".xlsx"), index=False)


if __name__ == "__main__":
    MUSIC_FORMATS: Final = frozenset([".mp3", ".wav", ".flac", ".ogg", ".m4a"])
    COLLECTION_DIR_PATH: Final = Path(__file__).parent.joinpath("catalog")
    COLLECTION_FILE_PATH: Final = Path(__file__).parent.joinpath(
        COLLECTION_DIR_PATH, "collection.csv"
    )

    while True:
        directory = Path(str(input("Enter directory to parse: ")))
        if directory.exists():
            break

        logging.error("No such directory")

    if not COLLECTION_DIR_PATH.exists():
        COLLECTION_DIR_PATH.mkdir()

    main(path=directory, file=COLLECTION_FILE_PATH)
