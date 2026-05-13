"""shared helper functions used across the project."""

from pathlib import Path
import pandas as pd
import numpy as np
import librosa

from src.config.settings import EMOTION_MAP, SPLIT_THRESHOLDS, SAMPLE_RATE, N_MELS, N_MFCC, N_FFT, HOP_LENGTH

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
        "emotion": EMOTION_MAP.get(emotion, "unknown"),
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
    if actor <= SPLIT_THRESHOLDS["train"]:
        return "train"
    elif actor <= SPLIT_THRESHOLDS["val"]:
        return "val"
    return "test"


def extract_mel(fp):
    """load wav and return log-mel spectrogram (transposed for 1d cnn).

    args:
        fp: str or pathlib.Path - path to wav file.

    returns:
        np.ndarray of shape (time_frames, n_mels) with log-mel values in db.
    """
    y, sr = librosa.load(fp, sr=SAMPLE_RATE)
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=N_MELS, n_fft=N_FFT, hop_length=HOP_LENGTH)
    return librosa.power_to_db(mel, ref=np.max).T


def extract_mfcc(fp):
    """load wav and return 240-dim mfcc feature vector for svm baseline.

    extracts 40 mfccs + delta + delta-delta, aggregates by mean and std.

    args:
        fp: str or pathlib.Path - path to wav file.

    returns:
        np.ndarray of shape (240,) - concatenated [mfcc_mean, mfcc_std,
        delta_mean, delta_std, delta2_mean, delta2_std].
    """
    y, sr = librosa.load(fp, sr=SAMPLE_RATE)
    m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC, n_fft=N_FFT, hop_length=HOP_LENGTH)
    d = librosa.feature.delta(m)
    d2 = librosa.feature.delta(m, order=2)
    return np.concatenate([m.mean(1), m.std(1), d.mean(1), d.std(1), d2.mean(1), d2.std(1)])
    