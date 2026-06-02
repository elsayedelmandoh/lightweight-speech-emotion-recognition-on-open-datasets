"""shared helper functions used across the project."""

import numpy as np
import librosa
from src.config.settings import SAMPLE_RATE, N_MELS, N_MFCC, N_FFT, HOP_LENGTH

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
    