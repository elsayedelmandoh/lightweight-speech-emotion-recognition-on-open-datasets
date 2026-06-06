"""Define typed settings and default configuration values using Pydantic."""

from pathlib import Path
from typing import Dict, List
import numpy as np
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Holds strongly-typed configurations for the Speech/Audio AI project."""

    # --- Base Directories ---
    BASE_DIR: Path = Field(default=Path(__file__).resolve().parents[2])

    # --- Pydantic Settings SettingsConfigDict ---
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Data Pipelines Storage ---
    RAW_DIR: Path = Field(default=Path("data/raw"))
    PROCESSED_DIR_NAME: Path = Field(default=Path("data/processed"))
    SAMPLES_DIR: Path = Field(default=Path("data/samples"))
    MODELS_DIR_NAME: Path = Field(default=Path("data/models"))
    PREDICTIONS_DIR_NAME: Path = Field(default=Path("data/predictions"))
    FIGURES_DIR_NAME: Path = Field(default=Path("docs/02-results/figures"))

    # --- Split Directories ---
    TRAIN_DIR_NAME: Path = Field(default=Path("data/train"))
    VAL_DIR_NAME: Path = Field(default=Path("data/val"))
    TEST_DIR_NAME: Path = Field(default=Path("data/test"))

    AUDIO_DIR_NAME: Path = Field(default=Path("data/processed/audio"))

    # --- Raw Audio Sub-directories ---
    RAW_SPEECH_DIR_NAME: Path = Field(default=Path("data/raw/Audio_Speech_Actors_01-24"))
    RAW_SONG_DIR_NAME: Path = Field(default=Path("data/raw/Audio_Song_Actors_01-24"))

    # --- Dataset & Split Definitions ---
    EMOTION_MAP: Dict[int, str] = Field(
        default={
            1: "neutral",
            2: "calm",
            3: "happy",
            4: "sad",
            5: "angry",
            6: "fearful",
        },
        frozen=True,
        description="Mapping from numerical labels to emotion names (6 shared emotions, song-compatible)"
    )

    CHANNEL_MAP: Dict[int, str] = Field(
        default={1: "speech", 2: "song"},
        frozen=True,
        description="Mapping from channel codes to channel names"
    )

    INTENSITY_MAP: Dict[int, str] = Field(
        default={1: "normal", 2: "strong"},
        frozen=True,
        description="Mapping from intensity codes to intensity descriptions"
    )

    SPLIT_THRESHOLDS: Dict[str, int] = Field(default={"train": 19, "val": 22})
    SPLIT_NAMES: List[str] = Field(default=["train", "val", "test"])

    EXPORT_COLS: List[str] = Field(default=["filepath", "split", "channel", "emotion_code", "emotion", "intensity", "actor", "gender", "statement", "repetition"])

    # --- GPU / Device ---
    DEVICE: str | None = Field(
        default=None,
        description="Override device ('cuda', 'cpu', 'mps'). Auto-detected if None."
    )

    @computed_field
    @property
    def TORCH_DEVICE(self) -> str:
        if self.DEVICE is not None:
            return self.DEVICE
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"

    # --- Audio Processing Hyperparameters ---
    # gt=Greater Than constraints ensure that these values must be positive
    SAMPLE_RATE: int = Field(default=16000, gt=0, description="Audio sampling rate in Hz")
    N_MELS: int = Field(default=128, gt=0, description="Number of Mel bands")
    N_MFCC: int = Field(default=40, gt=0, description="Number of MFCC features")
    N_FFT: int = Field(default=1024, gt=0, description="Length of the FFT window")
    HOP_LENGTH: int = Field(default=256, gt=0, description="Number of samples between successive STFT columns")
    DURATION: float = Field(default=4.0, description="Duration for fixed-length audio clips in seconds")
    TOP_DB: int = Field(default=25, description="Threshold in dB for silence trimming")
    PRE_EMPHASIS_COEF: float = Field(default=0.97, description="Pre-emphasis filter coefficient")
    RMS_NORM_CLIP: float = Field(default=3.0, description="RMS normalization clip threshold")

    # --- Feature Dimensionality ---
    N_MFCC_VECTOR: int = Field(default=240, gt=0, description="MFCC+delta+delta2 flattened dimension (6*N_MFCC)")
    N_MELS_FRAMES: int = Field(default=251, gt=0, description="Number of time frames per mel-spectrogram clip")
    DELTA_MEL_ORDER: int = Field(default=2, ge=0, description="Delta order for mel spectrogram stacking (0=no delta)")

    # --- Training Hyperparameters ---
    BATCH_SIZE: int = Field(default=32, gt=0, description="Training batch size")
    EPOCHS: int = Field(default=80, gt=0, description="Number of training epochs")
    NUM_CLASSES: int = Field(default=6, gt=0, description="Number of emotion classes (6 shared: neutral, calm, happy, sad, angry, fearful)")
    SEED: int = Field(default=42, description="Random seed for reproducibility")
    PATIENCE: int = Field(default=15, gt=0, description="Early stopping patience (epochs)")
    LEARNING_RATE: float = Field(default=1e-3, gt=0.0, description="Peak learning rate")
    WEIGHT_DECAY: float = Field(default=5e-4, ge=0.0, description="AdamW weight decay")
    LABEL_SMOOTHING: float = Field(default=0.05, ge=0.0, le=1.0, description="Label smoothing factor")
    CNN_DROPOUT: float = Field(default=0.3, ge=0.0, le=1.0, description="LightweightCNN1D dropout rate")

    # --- 1D CNN Training Hyperparameters ---
    CNN_1D_EPOCHS: int = Field(default=80, gt=0, description="Training epochs for 1D CNN on mel-spectrograms")
    CNN_1D_BATCH_SIZE: int = Field(default=32, gt=0, description="Batch size for 1D CNN")
    CNN_1D_PATIENCE: int = Field(default=20, gt=0, description="Early stopping patience for 1D CNN")
    SPEC_AUGMENT_TIME_MASK: int = Field(default=30, gt=0, description="SpecAugment max time mask width in frames")
    SPEC_AUGMENT_FREQ_MASK: int = Field(default=12, gt=0, description="SpecAugment max frequency mask width in mel bins")
    SPEC_AUGMENT_N_TIME: int = Field(default=2, ge=0, description="Number of time masks per sample")
    SPEC_AUGMENT_N_FREQ: int = Field(default=2, ge=0, description="Number of frequency masks per sample")

    # --- SVM Baseline Hyperparameters ---
    SVM_C: float = Field(default=1.0, gt=0.0, description="SVM regularization parameter (default for refit on full train)")
    SVM_PROBABILITY: bool = Field(default=True, description="Enable Platt scaling for SVM predict_proba (kept on; harmless if unused)")

    # --- Dynamic Computed Fields ---    
    @computed_field # these are computed on demand and not stored as instance attributes
    @property # call as variable, not method
    def DATA_DIR(self) -> Path:
        return self.BASE_DIR / "data"

    @computed_field
    @property
    def TRAIN_DIR(self) -> Path:
        return self.BASE_DIR / self.TRAIN_DIR_NAME

    @computed_field
    @property
    def VAL_DIR(self) -> Path:
        return self.BASE_DIR / self.VAL_DIR_NAME

    @computed_field
    @property
    def TEST_DIR(self) -> Path:
        return self.BASE_DIR / self.TEST_DIR_NAME

    @computed_field
    @property
    def AUDIO_TRAIN_DIR(self) -> Path:
        return self.BASE_DIR / self.AUDIO_DIR_NAME / self.TRAIN_DIR_NAME.name

    @computed_field
    @property
    def AUDIO_VAL_DIR(self) -> Path:
        return self.BASE_DIR / self.AUDIO_DIR_NAME / self.VAL_DIR_NAME.name

    @computed_field
    @property
    def AUDIO_TEST_DIR(self) -> Path:
        return self.BASE_DIR / self.AUDIO_DIR_NAME / self.TEST_DIR_NAME.name

    @computed_field
    @property
    def RAW_SPEECH_DIR(self) -> Path:
        return self.BASE_DIR / self.RAW_SPEECH_DIR_NAME

    @computed_field
    @property
    def RAW_SONG_DIR(self) -> Path:
        return self.BASE_DIR / self.RAW_SONG_DIR_NAME

    @computed_field
    @property
    def PROCESSED_DIR(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR_NAME

    @computed_field
    @property
    def LABELS_FILE(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR_NAME / "split_labels.csv"

    @computed_field
    @property
    def FEATURES_SPEECH_MEL(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR_NAME / "features_speech_mel.npy"

    @computed_field
    @property
    def FEATURES_SONG_MEL(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR_NAME / "features_song_mel.npy"

    @computed_field
    @property
    def FEATURES_SPEECH_MFCC(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR_NAME / "features_speech_mfcc.npy"

    @computed_field
    @property
    def FEATURES_SONG_MFCC(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR_NAME / "features_song_mfcc.npy"

    @computed_field
    @property
    def LABELS_SPEECH(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR_NAME / "labels_speech.npy"

    @computed_field
    @property
    def LABELS_SONG(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR_NAME / "labels_song.npy"

    @computed_field
    @property
    def N_SAMPLES(self) -> int:
        return int(self.SAMPLE_RATE * self.DURATION)

    @computed_field
    @property
    def TRAIN_ACTORS(self) -> List[int]:
        return list(range(1, 20))

    @computed_field
    @property
    def VAL_ACTORS(self) -> List[int]:
        return list(range(20, 23))

    @computed_field
    @property
    def TEST_ACTORS(self) -> List[int]:
        return list(range(23, 25))
    
    @computed_field
    @property
    def EMOTION_NAMES(self) -> List[str]:
        return list(self.EMOTION_MAP.values())

    @computed_field
    @property
    def MODELS_DIR(self) -> Path:
        return self.BASE_DIR / self.MODELS_DIR_NAME

    @computed_field
    @property
    def PREDICTIONS_DIR(self) -> Path:
        return self.BASE_DIR / self.PREDICTIONS_DIR_NAME

    @computed_field
    @property
    def FIGURES_DIR(self) -> Path:
        return self.BASE_DIR / self.FIGURES_DIR_NAME

    # --- Utilities ---
    def create_required_directories(self) -> None:
        """Bootstrap the directory tree on demand."""
        for dir_path in [
            self.DATA_DIR, self.RAW_DIR, self.SAMPLES_DIR,
            self.TRAIN_DIR, self.VAL_DIR, self.TEST_DIR,
            self.AUDIO_TRAIN_DIR, self.AUDIO_VAL_DIR, self.AUDIO_TEST_DIR,
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)
        # full-path computed fields
        self.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        self.RAW_SPEECH_DIR.mkdir(parents=True, exist_ok=True)
        self.RAW_SONG_DIR.mkdir(parents=True, exist_ok=True)
        self.MODELS_DIR.mkdir(parents=True, exist_ok=True)
        self.PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
        self.FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# Instantiate the singleton instance
settings = Settings()