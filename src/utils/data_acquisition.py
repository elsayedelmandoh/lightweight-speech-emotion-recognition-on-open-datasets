"""shared helper functions used across the project."""

from pathlib import Path
import pandas as pd
from src.config.config import settings


def count_wavs(dirpath):
    """count .wav files recursively in a directory.

    args:
        dirpath: pathlib.Path - directory to scan.

    returns:
        int - number of .wav files found, or 0 if dirpath is None or missing.
    """
    return sum(1 for _ in dirpath.rglob("*.wav")) if dirpath and dirpath.exists() else 0


def parse_filename(filepath):
    """parse a 7-part ravdess filename into a metadata dict.

    format: 03-CHANNEL-EMOTION-INTENSITY-STATEMENT-REPETITION-ACTOR.wav

    args:
        filepath: str or pathlib.Path - full path to a ravdess wav file.

    returns:
        dict with keys: filepath, channel, emotion_code, emotion, intensity,
        statement, repetition, actor, gender. returns None if filename
        does not have exactly 7 parts.
    """
    parts = Path(filepath).stem.split("-")
    if len(parts) != 7:
        return None
    _, channel, emotion, intensity, statement, rep, actor = map(int, parts)
    return {
        "filepath": str(filepath),
        "channel": "speech" if channel == 1 else "song",
        "emotion_code": emotion,
        "emotion": settings.EMOTION_MAP.get(emotion, "unknown"),
        "intensity": "normal" if intensity == 1 else "strong",
        "statement": statement,
        "repetition": rep,
        "actor": actor,
        "gender": "male" if actor % 2 == 1 else "female",
    }


def collect_wavs(source_dir):
    """walk actor subdirectories and parse all wavs into a dataframe.

    args:
        source_dir: pathlib.Path - directory containing Actor_XX/ subdirs.

    returns:
        pd.DataFrame with one row per wav file. columns match parse_filename keys.
    """
    records = []
    for actor_dir in sorted(source_dir.iterdir()):
        if not actor_dir.is_dir():
            continue
        for wav in actor_dir.glob("*.wav"):
            rec = parse_filename(wav)
            if rec:
                records.append(rec)
    return pd.DataFrame(records)


def assign_split(actor):
    """map actor id to train/val/test split.

    thresholds from settings.SPLIT_THRESHOLDS: train <= 19, val <= 22, else test.

    args:
        actor: int - actor id (01-24).

    returns:
        str - "train", "val", or "test".
    """
    if actor <= settings.SPLIT_THRESHOLDS["train"]:
        return "train"
    elif actor <= settings.SPLIT_THRESHOLDS["val"]:
        return "val"
    return "test"

def _get_dest(row):
    return str(settings.DATA_DIR / row["split"] / row["channel"] / f"Actor_{row['actor']:02d}" / Path(row["filepath"]).name)
