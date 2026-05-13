"""define typed settings and default configuration values."""

from pathlib import Path

# project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# raw data paths
RAW_SPEECH_DIR = RAW_DIR / "Audio_Speech_Actors_01-24"
RAW_SONG_DIR = RAW_DIR / "Audio_Song_Actors_01-24"

# split directories (after acquisition)
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"
TEST_DIR = DATA_DIR / "test"

# emotion label mapping
EMOTION_MAP = {
    1: "neutral",
    2: "calm",
    3: "happy",
    4: "sad",
    5: "angry",
    6: "fearful",
    7: "disgust",
    8: "surprised",
}

# speaker-disjoint split definition
SPLIT_THRESHOLDS = {"train": 19, "val": 22}
SPLIT_NAMES = ["train", "val", "test"]

# audio config 
SAMPLE_RATE = 48000
N_MELS = 128
N_MFCC = 40
N_FFT = 2048
HOP_LENGTH = 512
CLIP_DURATION_SEC = 3.0
CLIP_SAMPLES = int(SAMPLE_RATE * CLIP_DURATION_SEC)
TOP_DB = 20

# labels file 
LABELS_FILE = PROCESSED_DIR / "split_labels.csv"

# extracted feature paths 
FEATURES_SPEECH_MEL = PROCESSED_DIR / "features_speech_mel.npy"
FEATURES_SONG_MEL = PROCESSED_DIR / "features_song_mel.npy"
FEATURES_SPEECH_MFCC = PROCESSED_DIR / "features_speech_mfcc.npy"
FEATURES_SONG_MFCC = PROCESSED_DIR / "features_song_mfcc.npy"
LABELS_SPEECH = PROCESSED_DIR / "labels_speech.npy"
LABELS_SONG = PROCESSED_DIR / "labels_song.npy"

