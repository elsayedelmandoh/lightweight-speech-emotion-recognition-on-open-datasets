# repository structure and file responsibilities

## actual project structure

```text
project/
├── app.py                  # entrypoint (currently broken imports)
├── requirements.txt        # python dependencies
├── pyproject.toml          # build config, pytest config
├── .env.example            # env template (currently empty)
├── .gitignore              # fully commented out - nothing ignored!
├── opencode.json           # opencode cli config
├── src/
│   ├── __init__.py
│   ├── setup.py            # ensure_directories() helper
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py     # typed settings (stub)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py      # shared helpers (stub)
│   └── models/
│       └── __init__.py     # model definitions (empty)
├── notebooks/
│   ├── 00-quickstart.ipynb
│   ├── 01-data-acquisition/
│   ├── 02-eda/
│   ├── 03-data-preprocessing/
│   ├── 04-feature-engineering/
│   ├── 05-model-training/
│   ├── 06-model-evaluation/
│   └── 07-model-testing/
├── data/
│   ├── raw/                # original ravdess wavs
│   ├── processed/          # cleaned audio, feature arrays
│   ├── models/             # saved model checkpoints
│   ├── predictions/        # inference outputs
│   └── samples/            # small test fixtures
├── tests/                  # not yet created
└── docs/
    ├── 00-internal/
    ├── 01-project-definition/
    ├── 02-results/
    └── 03-deliverables/
```

## directory responsibilities

- `app.py`: entrypoint for local startup. currently non-functional due to broken imports.
- `src/config`: runtime configuration and environment loading. all hyperparameters go here.
- `src/utils`: shared utilities (data loading, label parsing, plotting). all notebooks import from here.
- `src/models`: model class definitions (cnn, svm wrapper). logic to be refactored from notebooks.
- `notebooks/`: primary workspace. numbered and sequential. stable logic gets migrated to `src/`.
- `data/raw`: source data, kept as close to original form as possible.
- `data/processed`: cleaned audio, extracted features (.npy arrays).
- `data/models`: serialized model artifacts (.pt, .pkl).
- `data/predictions`: output predictions and inference results.
- `data/samples`: small fixture-like datasets for fast iteration.
- `tests/`: unit and integration coverage. not yet created.

## import convention

```python
from src.config.settings import *
from src.utils.helpers import *
```

`settings.py` and `helpers.py` are currently stubs. populate them as logic is refactored out of notebooks.
