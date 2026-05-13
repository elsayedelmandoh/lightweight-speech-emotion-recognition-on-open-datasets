"""shared helper functions used across the project."""

from pathlib import Path
import pandas as pd
import numpy as np
import librosa

from src.config.settings import EMOTION_MAP, SPLIT_THRESHOLDS, SAMPLE_RATE, N_MELS, N_MFCC, N_FFT, HOP_LENGTH

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


# feature engineering step: extraction functions
def extract_mel(fp):
    y, sr = librosa.load(fp, sr=SAMPLE_RATE)
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=N_MELS, n_fft=N_FFT, hop_length=HOP_LENGTH)
    return librosa.power_to_db(mel, ref=np.max).T

def extract_mfcc(fp):
    y, sr = librosa.load(fp, sr=SAMPLE_RATE)
    m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC, n_fft=N_FFT, hop_length=HOP_LENGTH)
    d = librosa.feature.delta(m)
    d2 = librosa.feature.delta(m, order=2)
    return np.concatenate([m.mean(1), m.std(1), d.mean(1), d.std(1), d2.mean(1), d2.std(1)])
    