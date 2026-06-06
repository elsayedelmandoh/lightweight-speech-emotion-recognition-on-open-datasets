"""smoke tests to verify the project scaffold is wired up correctly."""

from pathlib import Path

import pytest


def test_src_config_imports():
    """verify src.config.config can be imported and instantiated."""
    from src.config.config import settings

    assert settings is not None


def test_src_setup_imports():
    """verify src.setup exposes the expected path getters and helpers."""
    from src.setup import (
        bootstrap_data_directories,
        get_data_dir,
        get_models_dir,
        get_project_root,
        get_src_dir,
        load_env_file,
    )

    root = get_project_root()
    assert root.is_dir()
    assert get_src_dir() == root / "src"
    assert get_data_dir() == root / "data"
    assert get_models_dir() == root / "data" / "models"
    assert callable(bootstrap_data_directories)
    assert callable(load_env_file)


def test_config_six_classes():
    """verify the 6-class emotion map matches the project scope."""
    from src.config.config import settings

    assert settings.NUM_CLASSES == 6
    assert len(settings.EMOTION_MAP) == 6
    for name in ("neutral", "calm", "happy", "sad", "angry", "fearful"):
        assert name in settings.EMOTION_MAP.values()


def test_speaker_disjoint_split():
    """verify train/val/test actor ranges are disjoint and cover 1-24."""
    from src.config.config import settings

    train = set(settings.TRAIN_ACTORS)
    val = set(settings.VAL_ACTORS)
    test = set(settings.TEST_ACTORS)
    assert train.isdisjoint(val)
    assert train.isdisjoint(test)
    assert val.isdisjoint(test)
    assert train | val | test == set(range(1, 25))


def test_audio_hyperparams_consistent():
    """verify audio hyperparameters satisfy n_samples = sample_rate * duration."""
    from src.config.config import settings

    assert settings.N_SAMPLES == int(settings.SAMPLE_RATE * settings.DURATION)
    assert settings.SAMPLE_RATE == 16000
    assert settings.DURATION == 4.0
    assert settings.N_MFCC_VECTOR == 6 * settings.N_MFCC


@pytest.mark.skipif(
    not Path("data/processed/X_test_mfcc.npy").exists(),
    reason="processed test set not found; run notebooks 03-04 first",
)
def test_svm_model_loads_and_predicts():
    """verify the trained svm baseline loads and predicts on the test set."""
    import joblib
    import numpy as np

    from src.setup import get_models_dir, get_processed_dir

    model = joblib.load(get_models_dir() / "svm_best.pkl")
    scaler = joblib.load(get_models_dir() / "mfcc_scaler.pkl")
    X_test = np.load(get_processed_dir() / "X_test_mfcc.npy")
    sample = scaler.transform(X_test[:1])
    pred = model.predict(sample)
    assert pred.shape == (1,)
    assert int(pred[0]) in range(6)
