"""bootstrap and packaging helpers for local development."""

import os
from pathlib import Path
from typing import Iterable


PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DIR: Path = DATA_DIR / "raw"
PROCESSED_DIR: Path = DATA_DIR / "processed"
MODELS_DIR: Path = DATA_DIR / "models"
PREDICTIONS_DIR: Path = DATA_DIR / "predictions"
SAMPLES_DIR: Path = DATA_DIR / "samples"

SRC_DIR: Path = PROJECT_ROOT / "src"
DOCS_DIR: Path = PROJECT_ROOT / "docs"
NOTEBOOKS_DIR: Path = PROJECT_ROOT / "notebooks"


def get_project_root() -> Path:
	return PROJECT_ROOT


def get_src_dir() -> Path:
	return SRC_DIR


def get_docs_dir() -> Path:
	return DOCS_DIR


def get_notebooks_dir() -> Path:
	return NOTEBOOKS_DIR


def get_data_dir() -> Path:
	return DATA_DIR


def get_raw_dir() -> Path:
	return RAW_DIR


def get_processed_dir() -> Path:
	return PROCESSED_DIR


def get_models_dir() -> Path:
	return MODELS_DIR


def get_predictions_dir() -> Path:
	return PREDICTIONS_DIR


def get_samples_dir() -> Path:
	return SAMPLES_DIR


def ensure_directories(paths: Iterable[Path]) -> None:
	for path in paths:
		path.mkdir(parents=True, exist_ok=True)


def bootstrap_data_directories() -> None:
	ensure_directories([
		RAW_DIR,
		PROCESSED_DIR,
		MODELS_DIR,
		PREDICTIONS_DIR,
		SAMPLES_DIR,
	])


def load_env_file(env_path: Path | None = None, *, overwrite: bool = False) -> int:
	"""load key=value pairs from a .env file into os.environ.

	lines starting with '#' and blank lines are ignored.
	values may optionally be wrapped in single or double quotes.
	by default, existing os.environ values are preserved (setdefault);
	pass overwrite=True to replace them instead.

	returns the number of variables loaded.
	"""
	if env_path is None:
		env_path = PROJECT_ROOT / ".env"
	if not env_path.exists():
		return 0
	loaded = 0
	for raw_line in env_path.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#"):
			continue
		if "=" not in line:
			continue
		key, _, value = line.partition("=")
		key = key.strip()
		value = value.strip()
		if len(value) >= 2 and (
			(value.startswith('"') and value.endswith('"'))
			or (value.startswith("'") and value.endswith("'"))
		):
			value = value[1:-1]
		if overwrite:
			os.environ[key] = value
		else:
			os.environ.setdefault(key, value)
		loaded += 1
	return loaded
