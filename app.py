"""application entrypoint for the project."""

from src.config.config import *
from src.setup import ensure_directories
from src.utils import *


def main() -> int:
	settings = load_settings()
	ensure_directories(settings.required_directories())

	pass


if __name__ == "__main__":
	raise SystemExit(main())
