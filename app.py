"""Application entrypoint for the lightweight speech emotion recognition
project.

This module loads the trained SVM baseline and runs a quick sanity check on a
random sample from the test set. Use this to verify the trained model loads
and predicts correctly before running the full evaluation pipeline.

Usage:
    python app.py
"""

import random
import sys

import joblib
import numpy as np

from src.config.config import settings
from src.setup import get_models_dir, get_processed_dir


def load_svm_model():
    """Load SVM + scaler from data/models/."""
    models_dir = get_models_dir()
    model_path = models_dir / "svm_best.pkl"
    scaler_path = models_dir / "mfcc_scaler.pkl"
    if not model_path.exists():
        sys.exit(f"SVM model not found at {model_path}. Run notebook 05.1 first.")
    if not scaler_path.exists():
        sys.exit(f"MFCC scaler not found at {scaler_path}. Run notebook 04 first.")
    return joblib.load(model_path), joblib.load(scaler_path)


def demo():
    """Predict on one random test sample as a sanity check."""
    model, scaler = load_svm_model()
    test_mfcc = get_processed_dir() / "X_test_mfcc.npy"
    test_labels = get_processed_dir() / "y_test.npy"
    if not test_mfcc.exists() or not test_labels.exists():
        sys.exit(f"Test set not found at {test_mfcc}. Run notebooks 03 and 04 first.")
    X_test = np.load(test_mfcc)
    y_test = np.load(test_labels)
    idx = random.Random(42).randrange(len(X_test))
    sample = scaler.transform(X_test[idx:idx + 1])
    pred = int(model.predict(sample)[0])
    true = int(y_test[idx])
    pred_name = settings.EMOTION_NAMES[pred]
    true_name = settings.EMOTION_NAMES[true]
    print(f"sample #{idx}: true={true_name}, predicted={pred_name}, match={pred == true}")
    print(f"model: svm (kernel={model.kernel}, c={model.C})")


if __name__ == "__main__":
    demo()
