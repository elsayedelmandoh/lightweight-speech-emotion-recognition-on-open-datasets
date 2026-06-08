"""svm model for mfcc-based speech emotion recognition (baseline).

the baseline required by the project definition: a classical support vector
machine on 240-dim mfcc feature vectors. uses rbf / linear / polynomial
kernels selected by gridsearch with 5-fold stratified cv.

public api:
    train_svm                  - fit standardscaler + gridsearchcv, return best model + scaler
    save_svm                   - persist svm + scaler to disk (svm_best.pkl + mfcc_scaler.pkl)
    load_svm                   - load svm + scaler from disk
    predict_svm                - inference: returns (preds, probs)
    cpu_inference_latency_svm  - per-sample cpu latency benchmark
"""

import time
from pathlib import Path
from typing import Optional, Tuple

import joblib
import numpy as np
from sklearn.model_selection import GridSearchCV, GroupKFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.config.config import settings


# default gridsearch parameter space (kernel + c + gamma combinations)
DEFAULT_PARAM_GRID = [
    {"kernel": ["rbf"],   "C": [0.1, 1], "gamma": [0.001, 0.005, 0.01, "scale"]},
    {"kernel": ["linear"], "C": [0.1, 1, 10]},
    {"kernel": ["poly"],  "degree": [2], "C": [1, 10], "gamma": ["scale", 0.01]},
]


def train_svm(
    X_train: np.ndarray,
    y_train: np.ndarray,
    groups: Optional[np.ndarray] = None,
    param_grid: Optional[list] = None,
    n_jobs: int = -1,
    cv_splits: int = 5,
    verbose: int = 2,
) -> Tuple[SVC, StandardScaler, dict]:
    """fit a standardscaler and gridsearch an svm classifier.

    args:
        X_train: training features, shape (n_samples, n_features)
        y_train: training labels, shape (n_samples,)
        groups: optional group labels (e.g., actor ids), shape (n_samples,).
            if provided, GroupKFold is used for cv (speaker-disjoint folds).
            if None, StratifiedKFold is used (random speaker-mixed folds).
        param_grid: list of param dicts (default: DEFAULT_PARAM_GRID)
        n_jobs: parallel jobs for gridsearch (-1 = all cores)
        cv_splits: number of cv splits
        verbose: gridsearch verbosity

    returns:
        (best_svm, scaler, cv_results) where:
            - best_svm is the sklearn SVC with the best cv score
            - scaler is the fitted StandardScaler (needed for inference)
            - cv_results is a dict with keys: best_score, best_params, best_estimator
    """
    if param_grid is None:
        param_grid = DEFAULT_PARAM_GRID

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    if groups is not None:
        cv = GroupKFold(n_splits=cv_splits)
    else:
        cv = StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=settings.SEED)
    grid = GridSearchCV(
        SVC(class_weight="balanced",
            probability=settings.SVM_PROBABILITY,
            random_state=settings.SEED),
        param_grid=param_grid,
        scoring="accuracy",
        cv=cv,
        n_jobs=n_jobs,
        verbose=verbose,
        return_train_score=False,
    )
    if groups is not None:
        grid.fit(X_scaled, y_train, groups=groups)
    else:
        grid.fit(X_scaled, y_train)

    cv_results = {
        "best_score":   float(grid.best_score_),
        "best_params":  grid.best_params_,
        "best_estimator": grid.best_estimator_,
    }
    return grid.best_estimator_, scaler, cv_results


def save_svm(
    model: SVC,
    scaler: StandardScaler,
    models_dir: Path,
    name: str = "svm_best",
    save_scaler_alias: bool = False,
) -> Tuple[Path, Path]:
    """save svm + scaler to disk.

    writes:
        {models_dir}/{name}.pkl       (the svm)
        {models_dir}/mfcc_scaler.pkl  (the scaler, fixed name)

    args:
        save_scaler_alias: if true, also write a generic `scaler.pkl` alias
            alongside (kept off by default; the canonical name is mfcc_scaler.pkl).

    returns:
        (svm_path, scaler_path)
    """
    models_dir = Path(models_dir)
    models_dir.mkdir(parents=True, exist_ok=True)

    svm_path = models_dir / f"{name}.pkl"
    scaler_path = models_dir / "mfcc_scaler.pkl"

    joblib.dump(model, svm_path)
    joblib.dump(scaler, scaler_path)
    if save_scaler_alias:
        joblib.dump(scaler, models_dir / "scaler.pkl")

    return svm_path, scaler_path


def load_svm(
    models_dir: Path,
    name: str = "svm_best",
    device: Optional[str] = None,
) -> Tuple[SVC, StandardScaler]:
    """load a saved svm + scaler from disk.

    args:
        models_dir: directory containing {name}.pkl and mfcc_scaler.pkl
        name: model name prefix (e.g. 'svm_best')
        device: ignored (kept for symmetry with load_cnn)

    returns:
        (svm, scaler)
    """
    models_dir = Path(models_dir)
    svm_path = models_dir / f"{name}.pkl"
    scaler_path = models_dir / "mfcc_scaler.pkl"

    model  = joblib.load(svm_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


def predict_svm(
    model: SVC,
    X: np.ndarray,
    scaler: Optional[StandardScaler] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """run svm inference.

    args:
        model: a fitted sklearn SVC
        X: features, shape (n_samples, n_features)
        scaler: optional StandardScaler to apply before prediction.
            if provided, X is transformed with scaler.transform(X).
            if None, X is used as-is (assumes already scaled).

    returns:
        (preds, probs) - preds shape (n_samples,), probs shape (n_samples, n_classes).
        probs requires the svm to have been trained with probability=True.
    """
    if scaler is not None:
        X = scaler.transform(X)
    preds = model.predict(X)
    probs = model.predict_proba(X)
    return preds, probs


def cpu_inference_latency_svm(
    model: SVC,
    n_runs: int = 50,
    device: str = "cpu",
) -> dict:
    """measure per-sample svm cpu inference latency in milliseconds.

    args:
        model: a fitted sklearn SVC
        n_runs: number of timed single-sample predictions
        device: reported in the output dict (svm is cpu-only)

    returns:
        dict with mean_ms, std_ms, p50_ms, p99_ms, n_runs, device.
    """
    X_dummy = np.random.randn(1, model.n_features_in_).astype(np.float32)

    # warmup
    for _ in range(10):
        _ = model.predict(X_dummy)

    timings = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        _ = model.predict(X_dummy)
        t1 = time.perf_counter()
        timings.append((t1 - t0) * 1000.0)

    timings = np.asarray(timings)
    return {
        "mean_ms": float(timings.mean()),
        "std_ms":  float(timings.std()),
        "p50_ms":  float(np.percentile(timings, 50)),
        "p99_ms":  float(np.percentile(timings, 99)),
        "n_runs":  n_runs,
        "device":  device,
    }
