"""Define typed settings and default configuration values using Pydantic."""

from pathlib import Path
from typing import Dict, List
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Holds strongly-typed configurations for the Speech/Audio AI project."""

    # --- Base Directories ---
    BASE_DIR: Path = Field(default=Path(__file__).resolve().parents[2])

    # --- Pydantic Settings SettingsConfigDict ---
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Data Pipelines Storage ---
    DATA_DIR: Path = Field(default=Path("data"))
    RAW_DIR: Path = Field(default=Path("data/raw"))
    PROCESSED_DIR: Path = Field(default=Path("data/processed"))
    SAMPLES_DIR: Path = Field(default=Path("data/samples"))
    
    # --- Split Directories ---
    TRAIN_DIR: Path = Field(default=Path("data/train"))
    VAL_DIR: Path = Field(default=Path("data/val"))
    TEST_DIR: Path = Field(default=Path("data/test"))

    # --- Raw Audio Sub-directories ---
    RAW_SPEECH_DIR: Path = Field(default=Path("data/raw/Audio_Speech_Actors_01-24"))
    RAW_SONG_DIR: Path = Field(default=Path("data/raw/Audio_Song_Actors_01-24"))

    # --- Results & Reporting ---
    FIGURES_DIR: Path = Field(default=Path("docs/02-results"))

    # --- Dataset & Split Definitions ---
    EMOTION_MAP: Dict[int, str] = Field(
        default={
            1: "neutral",
            2: "calm",
            3: "happy",
            4: "sad",
            5: "angry",
            6: "fearful",
            7: "disgust",
            8: "surprised",
        },
        frozen=True,
        description="Mapping from numerical labels to emotion names"
    )

    SPLIT_THRESHOLDS: Dict[str, int] = Field(default={"train": 19, "val": 22})
    SPLIT_NAMES: List[str] = Field(default=["train", "val", "test"])

    # --- Audio Processing Hyperparameters ---
    # gt=Greater Than constraints ensure that these values must be positive
    SAMPLE_RATE: int = Field(default=48000, gt=0, description="Audio sampling rate in Hz")
    N_MELS: int = Field(default=128, gt=0, description="Number of Mel bands")
    N_MFCC: int = Field(default=40, gt=0, description="Number of MFCC features")
    N_FFT: int = Field(default=2048, gt=0, description="Length of the FFT window")
    HOP_LENGTH: int = Field(default=512, gt=0, description="Number of samples between successive STFT columns")
    CLIP_DURATION_SEC: float = Field(default=3.0, gt=0.0, description="Target duration for audio clips in seconds")
    TOP_DB: int = Field(default=20, description="Threshold for decibel-based trimming")

    # --- Dynamic Computed Fields ---    
    @computed_field # these are computed on demand and not stored as instance attributes
    @property # call as variable, not method
    def LABELS_FILE(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR / "split_labels.csv"

    @computed_field
    @property
    def FEATURES_SPEECH_MEL(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR / "features_speech_mel.npy"

    @computed_field
    @property
    def FEATURES_SONG_MEL(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR / "features_song_mel.npy"

    @computed_field
    @property
    def FEATURES_SPEECH_MFCC(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR / "features_speech_mfcc.npy"

    @computed_field
    @property
    def FEATURES_SONG_MFCC(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR / "features_song_mfcc.npy"

    @computed_field
    @property
    def LABELS_SPEECH(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR / "labels_speech.npy"

    @computed_field
    @property
    def LABELS_SONG(self) -> Path:
        return self.BASE_DIR / self.PROCESSED_DIR / "labels_song.npy"

    # --- Utilities ---
    def create_required_directories(self) -> None:
        """Bootstrap the directory tree on demand."""
        directories = [
            self.DATA_DIR, self.RAW_DIR, self.PROCESSED_DIR, self.SAMPLES_DIR,
            self.TRAIN_DIR, self.VAL_DIR, self.TEST_DIR,
            self.RAW_SPEECH_DIR, self.RAW_SONG_DIR, self.FIGURES_DIR
        ]
        for dir_path in directories:
            actual_path = self.BASE_DIR / dir_path
            actual_path.mkdir(parents=True, exist_ok=True)

# Instantiate the singleton instance
settings = Settings()