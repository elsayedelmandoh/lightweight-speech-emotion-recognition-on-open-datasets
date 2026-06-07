"""helper functions for exploratory data analysis."""

import pandas as pd
from src.config.config import settings


def load_labels() -> pd.DataFrame:
    """load split_labels.csv into a DataFrame.

    returns:
        pd.DataFrame with columns: filepath, split, channel,
        emotion_code, emotion, intensity, actor, gender,
        statement, repetition.
    """
    return pd.read_csv(settings.LABELS_FILE)
