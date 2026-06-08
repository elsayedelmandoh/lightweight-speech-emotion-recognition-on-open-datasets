"""shared helper functions for audio preprocessing."""

from pathlib import Path
import numpy as np
import librosa
import pandas as pd
from src.config.config import settings
from src.utils.data_acquisition import parse_filename as _parse_filename_canonical


def preprocess_audio(filepath, sr=None, n_samples=None, top_db=None,
                     pre_emphasis=None, rms_clip=None):
    """load + resample + pre-emphasis + trim silence + rms norm + fixed length.

    args:
        filepath: str or Path - path to wav file.
        sr: sample rate (default: settings.SAMPLE_RATE).
        n_samples: target length (default: settings.N_SAMPLES).
        top_db: silence threshold (default: settings.TOP_DB).
        pre_emphasis: filter coefficient (default: settings.PRE_EMPHASIS_COEF).
        rms_clip: normalization clip (default: settings.RMS_NORM_CLIP).

    returns:
        np.ndarray of shape (n_samples,) with dtype float32.
    """
    if sr is None:
        sr = settings.SAMPLE_RATE
    if n_samples is None:
        n_samples = settings.N_SAMPLES
    if top_db is None:
        top_db = settings.TOP_DB
    if pre_emphasis is None:
        pre_emphasis = settings.PRE_EMPHASIS_COEF
    if rms_clip is None:
        rms_clip = settings.RMS_NORM_CLIP

    audio, _ = librosa.load(filepath, sr=sr, mono=True)
    audio = np.append(audio[0], audio[1:] - pre_emphasis * audio[:-1])
    audio, _ = librosa.effects.trim(audio, top_db=top_db)
    rms = np.sqrt(np.mean(audio ** 2))
    if rms > 0:
        audio = audio / (rms + 1e-8)
        audio = np.clip(audio, -rms_clip, rms_clip)
        audio = audio / rms_clip
    if len(audio) < n_samples:
        audio = np.pad(audio, (0, n_samples - len(audio)))
    else:
        audio = audio[:n_samples]
    return audio.astype(np.float32)


def parse_filename(filepath):
    """parse a 7-part ravdess filename into metadata dict with emotion_id.

    delegates to the canonical parser in src.utils.data_acquisition, then
    adds a 0-indexed emotion_id for downstream filtering.

    args:
        filepath: str or Path.

    returns:
        dict with keys: filepath, channel, emotion, emotion_id, actor.
        returns None if filename does not have exactly 7 parts.
    """
    meta = _parse_filename_canonical(filepath)
    if meta is None:
        return None
    return {
        'filepath':  meta['filepath'],
        'channel':   meta['channel'],
        'emotion':   meta['emotion'],
        'emotion_id': meta['emotion_code'] - 1,
        'actor':     meta['actor'],
    }


def build_split_dataframe(raw_dir):
    """walk raw dir, parse wav files, build full dataframe with actor-based splits.

    args:
        raw_dir: Path to raw audio directory.

    returns:
        tuple of (train_df, val_df, test_df) with parsed metadata.
    """
    records = []
    for wav_file in sorted(Path(raw_dir).rglob('*.wav')):
        info = parse_filename(wav_file)
        if info:
            records.append(info)
    df = pd.DataFrame(records)
    df = df[df['emotion_id'].between(0, settings.NUM_CLASSES - 1)].reset_index(drop=True)
    train_df = df[df['actor'].isin(settings.TRAIN_ACTORS)].reset_index(drop=True)
    val_df = df[df['actor'].isin(settings.VAL_ACTORS)].reset_index(drop=True)
    test_df = df[df['actor'].isin(settings.TEST_ACTORS)].reset_index(drop=True)
    return train_df, val_df, test_df


def save_split(split_df, audio_dir, split_name):
    """preprocess audio rows and write .npy under {audio_dir}/{channel}/Actor_{actor:02d}/{stem}.npy. returns (saved, errors)."""
    saved = 0
    errors = 0
    for _, row in split_df.iterrows():
        try:
            audio = preprocess_audio(row['filepath'])
            actor = int(row['actor'])
            out_dir = Path(audio_dir) / row['channel'] / f"Actor_{actor:02d}"
            out_dir.mkdir(parents=True, exist_ok=True)
            stem = Path(row['filepath']).stem
            out_path = out_dir / f"{stem}.npy"
            np.save(out_path, audio)
            saved += 1
        except Exception:
            errors += 1
    return saved, errors
