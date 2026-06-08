# repository structure and file responsibilities

## project structure

```
lightweight-speech-emotion-recognition-on-open-datasets/
├── app.py                  # entrypoint (currently broken imports)
├── requirements.txt        # python dependencies
├── pyproject.toml          # build config, pytest config
├── .env.example            # env template (currently empty)
├── .gitignore              # fully commented out - nothing ignored!
├── src/
│   ├── config/
│   │   └── config.py       # typed settings, paths, hyperparameters (populated)
│   └── utils/
│       ├── data_acquisition.py     # data loading, filename parsing, split assignment
│       ├── data_preprocessing.py   # audio preprocessing
│       ├── eda.py                  # exploratory data analysis helpers
│       └── feature_engineering.py  # mel/mfcc feature extraction
├── notebooks/
│   ├── 00-quickstart.ipynb
│   ├── 01-data-acquisition/
│   ├── 02-eda/
│   ├── 03-data-preprocessing/
│   ├── 04-feature-engineering/
│   ├── 05-model-training/
│   ├── 06-model-evaluation/
│   ├── 07-model-testing/
│   └── 00-preliminary-experiments/    # sample-based rapid pipeline
│       ├── 00-quickstart.ipynb
│       ├── 01-data-acquisition.ipynb
│       ├── 02-eda.ipynb
│       ├── 03-data-preprocessing.ipynb
│       ├── 04-feature-engineering.ipynb
│       ├── 05-model-training.ipynb
│       ├── 06-model-evaluation.ipynb
│       └── 07-model-testing.ipynb
├── data/
│   ├── raw/                # original ravdess download (video + audio)
│   ├── train/              # training: speech/ + song/ per actor
│   ├── val/                # validation: speech/ + song/ per actor
│   ├── test/               # held-out test: speech/ + song/ per actor
│   ├── processed/          # split_labels.csv, feature .npy arrays
│   ├── samples/            # sample subset (4 actors, 416 files) for rapid iteration
│   ├── models/             # saved model artifacts (.pkl, .pt)
│   └── predictions/        # inference outputs (.csv)
├── docs/
│   ├── 00-internal/
│   │   └── plan/
│   │       └── 01-specs.md    # detailed member specs
│   ├── 01-project-definition/  # all files populated
│   │   ├── 00-quickstart.md
│   │   ├── 01-problem.md
│   │   ├── 02-goal.md
│   │   ├── 03-related-work.md
│   │   ├── 04-research-notes.md
│   │   ├── 05-dataset.md
│   │   ├── 06-solution.md
│   │   ├── 07-constraints.md
│   │   ├── 08-architecture.md
│   │   ├── 09-stack.md
│   │   ├── 10-structure.md
│   │   ├── 11-workflow.md
│   │   ├── 12-timeline.md
│   │   └── 13-references.md
│   ├── 02-results/             # figures and analysis docs
│   │   ├── 00-quickstart.md
│   │   ├── 01-evaluation.md
│   │   ├── 02-testing.md
│   │   ├── 03-performance-comparison.md
│   │   ├── 04-results-analysis.md
│   │   ├── 05-future-work.md
│   │   ├── fig01-svm-confusion-matrix.png
│   │   ├── fig02-per-class-f1.png
│   │   ├── fig03-emotion-distribution.png
│   │   ├── fig04-sample-waveforms.png
│   │   ├── fig05-mel-spectrograms.png
│   │   └── fig06-timing-breakdown.png
│   └── 03-deliverables/
│       ├── 01-midterm-report/
│       │   ├── 01-title-and-abstract.md
│       │   ├── 02-introduction.md
│       │   ├── 03-related-work.md
│       │   ├── 04-methodology.md
│       │   ├── 05-preliminary-experiments-and-results.md
│       │   ├── 06-planned-work-and-timeline.md
│       │   ├── 07-team-contributions.md
│       │   ├── 08-references.md
│       │   └── 09-midterm-report.md
│       ├── 02-final-report/
│       └── 03-presentation/
```

## directory responsibilities

- `app.py`: entrypoint for local startup. currently non-functional due to broken imports.
- `src/config/`: runtime configuration, paths, hyperparameters in `config.py`.
- `src/utils/`: shared functions: `data_acquisition.py` (parse_filename, collect_wavs, assign_split), `data_preprocessing.py` (preprocess_audio, save_split), `feature_engineering.py` (extract_logmel, extract_mfcc_vector), `eda.py` (load_labels). notebooks import from here.
- `src/models/`: model class definitions (empty - refactoring planned from notebooks).
- `notebooks/00-preliminary-experiments/`: full pipeline on a 416-file sample subset. each notebook is self-contained and runs in minutes.
- `notebooks/01-07`: full-scale pipeline directories (stubs, awaiting population).
- `data/raw/`: original zenodo download (2452 audio-only + video files).
- `data/{train,val,test}/`: speaker-disjoint split. each has `speech/` and `song/` subdirectories.
- `data/processed/`: `split_labels.csv` (all metadata), `.npy` feature arrays.
- `data/samples/`: mini dataset (actors 01,02 for train, 20 for val, 23 for test - 416 files) for fast iteration.
- `data/models/`: serialized model artifacts (.pkl for svm, planned .pt for cnn).
- `data/predictions/`: inference outputs as .csv with per-clip predictions.

## import convention

```python
from src.config.config import settings
from src.utils.data_acquisition import parse_filename, collect_wavs, assign_split
from src.utils.data_preprocessing import preprocess_audio, build_split_dataframe
from src.utils.feature_engineering import extract_logmel, extract_mfcc_vector
```

the actual import convention varies by notebook: notebooks import specific functions from the relevant utils modules. the `settings` singleton from `src.config.config` is the canonical path. there is no `helpers.py` or `settings.py` -- they were split into purpose-specific files during refactoring.
