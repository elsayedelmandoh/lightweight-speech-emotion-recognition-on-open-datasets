"""application entrypoint for the project."""

from src.config.setting import variable
from src.utils..helpers import build_database_url


def main() -> int:
	settings = load_settings()
	ensure_directories(settings.required_directories())

	database_url = build_database_url(settings.database_url, settings.data_dir / "base_product.db")

	print(f"project: {settings.project_name}")
	print(f"environment: {settings.environment}")
	print(f"database: {database_url}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
