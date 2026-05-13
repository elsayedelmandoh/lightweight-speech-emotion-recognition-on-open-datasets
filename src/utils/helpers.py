"""shared helper functions used across the project."""

from pathlib import Path
import pandas as pd

from src.config.settings import EMOTION_MAP, SPLIT_THRESHOLDS


def count_wavs(dirpath):
    return sum(1 for _ in dirpath.rglob("*.wav")) if dirpath and dirpath.exists() else 0


def parse_filename(filepath):
    parts = Path(filepath).stem.split("-")
    if len(parts) != 7:
        return None
    _, channel, emotion, intensity, statement, rep, actor = map(int, parts)
    return {
        "filepath": str(filepath),
        "channel": "speech" if channel == 1 else "song",
        "emotion_code": emotion,
        "emotion": EMOTION_MAP.get(emotion, "unknown"),
        "intensity": "normal" if intensity == 1 else "strong",
        "statement": statement,
        "repetition": rep,
        "actor": actor,
        "gender": "male" if actor % 2 == 1 else "female",
    }


def collect_wavs(source_dir):
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
    if actor <= SPLIT_THRESHOLDS["train"]:
        return "train"
    elif actor <= SPLIT_THRESHOLDS["val"]:
        return "val"
    return "test"

