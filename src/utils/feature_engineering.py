"""shared helper functions for feature extraction.

provides two interfaces:
- filepath-based (loads wav directly via librosa)
- array-based (operates on preprocessed audio arrays)

main features used by the project:
- log-mel-spectrogram (128 mel x 251 frames) -> 1d cnn input
- mfcc + delta + delta2 vector (240-dim) -> svm baseline
- audio-level augmentation utilities
"""

from pathlib import Path
import numpy as np
import librosa
from tqdm import tqdm
from src.config.config import settings

def extract_mel(fp):
    """load wav and return log-mel spectrogram (transposed for 1d cnn).

    args:
        fp: str or pathlib.Path - path to wav file.

    returns:
        np.ndarray of shape (time_frames, n_mels) with log-mel values in db.
    """
    y, sr = librosa.load(fp, sr=settings.SAMPLE_RATE)
    mel = librosa.feature.melspectrogram(
        y=y, sr=sr, n_mels=settings.N_MELS,
        n_fft=settings.N_FFT, hop_length=settings.HOP_LENGTH)
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
    y, sr = librosa.load(fp, sr=settings.SAMPLE_RATE)
    m = librosa.feature.mfcc(
        y=y, sr=sr, n_mfcc=settings.N_MFCC,
        n_fft=settings.N_FFT, hop_length=settings.HOP_LENGTH)
    d = librosa.feature.delta(m)
    d2 = librosa.feature.delta(m, order=2)
    return np.concatenate([
        m.mean(1), m.std(1), d.mean(1), d.std(1),
        d2.mean(1), d2.std(1)])


def extract_logmel(audio, sr=None, n_mels=None, n_fft=None, hop_len=None):
    """compute log-mel spectrogram from preprocessed audio array.

    applies per-sample normalization (zero mean, unit std) so the cnn
    can train on inputs with consistent scale.

    args:
        audio: 1d np.ndarray of audio samples.
        sr: sample rate (default: settings.SAMPLE_RATE).
        n_mels: mel bands count (default: settings.N_MELS).
        n_fft: fft window (default: settings.N_FFT).
        hop_len: hop length (default: settings.HOP_LENGTH).

    returns:
        np.ndarray of shape (n_mels, time_frames) float32.
    """
    if sr is None:
        sr = settings.SAMPLE_RATE
    if n_mels is None:
        n_mels = settings.N_MELS
    if n_fft is None:
        n_fft = settings.N_FFT
    if hop_len is None:
        hop_len = settings.HOP_LENGTH

    mel = librosa.feature.melspectrogram(
        y=audio, sr=sr, n_mels=n_mels,
        n_fft=n_fft, hop_length=hop_len,
        fmin=20, fmax=8000)
    mel_db = librosa.power_to_db(mel + 1e-10, ref=np.max)
    mel_db = np.nan_to_num(mel_db, nan=0.0, posinf=0.0, neginf=0.0)
    mean = mel_db.mean()
    std = mel_db.std()
    mel_db = (mel_db - mean) / (std + 1e-8)
    return mel_db.astype(np.float32)


def extract_mfcc_vector(audio, sr=None, n_mfcc=None):
    """compute 240-dim mfcc + delta + delta2 vector from preprocessed audio.

    args:
        audio: 1d np.ndarray of audio samples.
        sr: sample rate (default: settings.SAMPLE_RATE).
        n_mfcc: coefficient count (default: settings.N_MFCC).

    returns:
        np.ndarray of shape (240,) float32.
    """
    if sr is None:
        sr = settings.SAMPLE_RATE
    if n_mfcc is None:
        n_mfcc = settings.N_MFCC

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    delta = librosa.feature.delta(mfcc)
    delta2 = librosa.feature.delta(mfcc, order=2)
    return np.concatenate([
        np.mean(mfcc, axis=1), np.std(mfcc, axis=1),
        np.mean(delta, axis=1), np.std(delta, axis=1),
        np.mean(delta2, axis=1), np.std(delta2, axis=1),
    ]).astype(np.float32)


def get_label(filepath):
    """extract 0-indexed emotion label from ravdess filename.

    args:
        filepath: str or Path - path to audio file.

    returns:
        int 0-7 (neutral=0, calm=1, ..., surprised=7).

    raises:
        ValueError: if filename does not have a valid RAVDESS-format
            emotion code (third dash-separated component).
    """
    filename = Path(filepath).stem
    parts = filename.split('-')
    if len(parts) < 3 or not parts[2].isdigit():
        raise ValueError(
            f"Cannot parse emotion label from '{filepath}': "
            f"expected RAVDESS-format filename (e.g. 03-01-01-...). "
            f"Got parts={parts}"
        )
    emotion_code = int(parts[2])
    return emotion_code - 1


def augment_gaussian_noise(audio, noise_level=0.005):
    """add gaussian noise."""
    noise = np.random.randn(len(audio)) * noise_level
    return audio + noise


def augment_pitch_shift(audio, sr=None, n_steps=None):
    """shift pitch by +/-2 semitones."""
    if sr is None:
        sr = settings.SAMPLE_RATE
    if n_steps is None:
        n_steps = np.random.choice([-2, -1, 1, 2])
    return librosa.effects.pitch_shift(y=audio, sr=sr, n_steps=n_steps)


def augment_time_stretch(audio, rate=None):
    """time stretch by factor 0.9-1.1."""
    if rate is None:
        rate = np.random.uniform(0.9, 1.1)
    return librosa.effects.time_stretch(y=audio, rate=rate)


def augment_audio(audio, sr=None):
    """apply random combination of augmentation to audio."""
    if sr is None:
        sr = settings.SAMPLE_RATE
    aug = audio.copy()
    if np.random.rand() > 0.5:
        aug = augment_gaussian_noise(aug)
    if np.random.rand() > 0.5:
        aug = augment_pitch_shift(aug, sr=sr)
    if np.random.rand() > 0.5:
        aug = augment_time_stretch(aug)
    if len(aug) < len(audio):
        aug = np.pad(aug, (0, len(audio) - len(aug)))
    elif len(aug) > len(audio):
        aug = aug[:len(audio)]
    return aug


def extract_all_logmel(data_dir, split_name):
    """extract log-mel from all .npy files in a directory.

    args:
        data_dir: Path to dir with .npy audio arrays (subdirs per channel).
        split_name: str label for tqdm progress bar.

    returns:
        tuple (X, y) where X is (n_samples, n_mels, time_frames)
        and y is (n_samples,) int labels.
    """
    X, y = [], []
    for npy_file in tqdm(sorted(Path(data_dir).rglob('*.npy')),
                         desc=f'LogMel {split_name}'):
        try:
            audio = np.load(npy_file)
            mel = extract_logmel(audio)
            label = get_label(npy_file)
            X.append(mel)
            y.append(label)
        except Exception:
            pass
    return np.array(X), np.array(y)


def extract_all_mfcc(data_dir, split_name):
    """extract mfcc vectors from all .npy files in a directory.

    args:
        data_dir: Path to dir with .npy audio arrays.
        split_name: str label for tqdm progress bar.

    returns:
        tuple (X, y) where X is (n_samples, 240) and y is (n_samples,) int.
    """
    X, y = [], []
    for npy_file in tqdm(sorted(Path(data_dir).rglob('*.npy')),
                         desc=f'MFCC {split_name}'):
        try:
            audio = np.load(npy_file)
            mfcc = extract_mfcc_vector(audio)
            label = get_label(npy_file)
            X.append(mfcc)
            y.append(label)
        except Exception:
            pass
    return np.array(X), np.array(y)
