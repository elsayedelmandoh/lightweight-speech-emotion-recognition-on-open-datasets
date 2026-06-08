# Development Log

> Weekly progress, key decisions, and issues encountered.
> Maintained as required by project policy (§4 - Process Documentation).
> Every entry is traceable to Git commit hashes.

---

## Week 1 — Project Scaffolding & Data Understanding (May 7–10, 2026)

### Progress

- **Initialized repository** with full project skeleton: README, LICENSE (MIT), `.gitignore`, `app.py` scaffold, directory structure for data (raw/processed/models/predictions/samples), and draft project-definition documents (problem statement, goals, solution overview, dataset description, constraints, tech stack, directory structure, workflow, architecture).
- **Cleaned up scaffolding**: removed `.internal/` directory (contained AGENTS.md, Claude config, and skill definitions) — these were AI-agent support files not needed in the student repo.
- **Khaled** contributed research notes on available dataset options and began documenting MFCC-based audio feature extraction for the classical baseline.
- **Defined core preprocessing parameters**: 128 mel bands, 40 MFCC coefficients, 2048 FFT window, 512 hop length, 48 kHz sample rate, 3-second clip duration.
- **Set up data directory structure**: raw data directories for speech (`Audio_Speech_Actors_01-24`) and song (`Audio_Song_Actors_01-24`), plus train/val/test split directories.

### Key Decisions

- **RAVDESS as primary dataset** — smaller and more widely benchmarked than alternatives (CREMA-D, TESS). 24 actors, 8 emotions, speech + song channels.
- **Speaker-disjoint split**: actors 1–19 train / 20–22 val / 23–24 test. This ensures cross-speaker generalization is measured honestly, avoiding inflated metrics from speaker overlap.
- **6-class subset** selected for initial experiments (neutral, calm, happy, sad, angry, fearful), dropping disgust and surprised. This aligns with the song channel's 6-emotion schema and simplifies cross-channel comparison.
- **Two-model comparison design**: CNN on log-mel spectrograms (deep) vs. SVM on MFCC+delta statistics (classical baseline).

### Issues Encountered

- None in this phase — still in documentation and planning stage.

### Relevant Commits

| Commit | Author | Description |
|--------|--------|-------------|
| `99a0289` | Elsayed Elmandoh | First commit: full repo scaffold, docs, config |
| `193285f` | Elsayed Elmandoh | Cleanup: removed `.internal/` agent config dir |
| `77e67d8` | Khaled Ashoush | Added data research notes for options |
| `55d1c34` | Khaled Ashoush | Added MFCC notes for audio preprocessing |
| `a25594a` | Elsayed Elmandoh | Finalized Week 1 project definitions |

---

## Week 2 — Midterm Report & Notebook Pipeline (May 12–13, 2026)

### Progress

- **Khaled** documented the full RAVDESS filename convention in `docs/01-project-definition/05-dataset.md` — the 7-part numeric encoding (modality / channel / emotion / intensity / statement / repetition / actor).
- **Expanded all project-definition documents** significantly (~525 lines added, 176 modified): quickstart guide, problem statement, goals, related work, research notes, dataset details, solution approach, constraints, architecture, stack, structure, and workflow.
- **Drafted initial midterm report content**: Title & Abstract, Introduction, and Related Work sections.
- **Created midterm report infrastructure**: quickstart guide, team contributions template, references section, and generated IEEE-format outline.
- **Scaffolded the full Jupyter notebook pipeline** (7 notebooks):
  1. Data acquisition (download + speaker-disjoint split)
  2. Exploratory Data Analysis
  3. Data preprocessing (trimming, normalization, padding)
  4. Feature engineering (mel spectrograms + MFCCs)
  5. Model training (CNN + SVM)
  6. Model evaluation (metrics, confusion matrices)
  7. Model testing (held-out test set)
- **Created `src/config/settings.py`** — typed configuration with Path-based directory settings, emotion label map, audio parameters, and split definitions.
- **Created `src/utils/helpers.py`** — shared utilities including `parse_filename()` (RAVDESS filename parser), `count_wavs()`, and audio loading helpers.
- **Added `requirements.txt`** with core dependencies (torch, librosa, scikit-learn, numpy, pandas, matplotlib, seaborn, jupyter).

### Key Decisions

- **Notebook order is hard dependency**: each notebook consumes the output of its predecessor. Documented in workflow as a directed acyclic graph.
- **Utility code extracted to `src/`** rather than duplicated across notebooks, enabling reuse in test scripts and the Streamlit app.
- **RAVDESS filename parser designed** to handle all 7 identifier fields, enabling automated label extraction without manual annotation.

### Issues Encountered

- Several notebooks existed as stubs only — the actual computation code was written later. The pipeline structure was correct but empty implementations remained until Week 3.
- Configuration was in a raw `settings.py` module rather than a validated model — refactored to Pydantic-based `config.py` in Week 3.

### Relevant Commits

| Commit | Author | Description |
|--------|--------|-------------|
| `e93456a` | Khaled Ashoush | Documented RAVDESS filename convention & identifier breakdown |
| `94e9d1b` | Elsayed Elmandoh | Mass expansion of project-definition docs (12 files) |
| `eaa0f8f` | Elsayed Elmandoh | Created midterm report: Title & Abstract, Introduction, Related Work |
| `4488a8d` | Elsayed Elmandoh | Midterm report quickstart + Team Contributions + References |
| `61e2f14` | Elsayed Elmandoh | Refined quickstart and midterm Abstract/Introduction |
| `b325115` | Elsayed Elmandoh | Scaffolded all 7 notebooks + config/settings.py + helpers.py |
| `5a9e578` | Elsayed Elmandoh | Finalized Week 2 state |

---

## Week 3 — Model Implementation, Training & Evaluation (June 2–7, 2026)

### Progress

**June 2 — Midterm submission & notebook refactoring:**
- Uploaded completed **midterm report** (Markdown + PDF) with workflow diagrams.
- Renamed `src/utils/helpers.py` → `data_acquistion.py` (note: filename typo kept for compatibility).
- Created **`src/utils/feature_engineering.py`** (232 lines) — full feature extraction: log-mel spectrograms via `extract_mel()`, MFCC+delta statistics via `extract_mfcc()`, and batched dataset-level extraction.
- Created **`src/config/config.py`** — refactored from plain `settings.py` to **Pydantic v2 `BaseSettings`** with `.env` support, computed fields, and strongly-typed path resolution.
- Created comparison analysis notebook structure.

**June 3 — First data pipeline execution:**
- Ran data acquisition: generated `split_labels.csv`, `sample_labels.csv`, `predictions_sample.csv`, and `scaler.pkl`.
- Generated processed feature arrays (mel spectrograms + MFCC vectors for speech channel).
- Cleaned up intermediate files.

**June 6 — Model training & evaluation (major milestone):**
- Implemented **`src/models/cnn1d_model.py`** (402 lines):
  - `LightweightCNN1D`: 3-block Conv1D architecture (~132K params, <600KB on disk)
  - `MelSpectrogramDataset` with **SpecAugment** (time + frequency masking)
  - `train_cnn()`: full training loop with AdamW + OneCycleLR + label smoothing (0.05) + early stopping
  - `save_cnn()` / `load_cnn()` / `predict_cnn()` for persistence and inference
  - `cpu_inference_latency()` benchmark utility
- Implemented **`src/models/svm_model.py`** (219 lines):
  - `train_svm()`: StandardScaler + GridSearchCV (RBF/linear/poly kernels, 5-fold stratified CV)
  - `save_svm()` / `load_svm()` / `predict_svm()` with `cpu_inference_latency_svm()`
- **Trained both models** on the speech 6-class scenario:
  - **CNN1D**: 80 epochs (early stopping at 67), best val accuracy 75.38%
  - **SVM**: GridSearch selected RBF kernel with C=1.0
- **Generated full evaluation results**: per-class accuracy, confusion matrices, CPU latency benchmarks for both models on val set.
- Added **`tests/test_smoke.py`** (85 lines) — basic smoke tests ensuring imports, data loading, and model forward pass work.
- Created **`pyproject.toml`** and **`src/setup.py`** for pip-installable package structure.
- Updated **README** with comprehensive project overview, key features, methodology, results figures, and badges.
- Added reference paper: "Speech Emotion Recognition Based on Multiple Acoustic Features" (full text + PDF).
- Removed the deprecated `data_acquistion.py` utility (moved logic into notebook pipeline).

**June 7 — Salma completed EDA & data preprocessing:**
- Completed full **EDA notebook** (`02-eda.ipynb`, +499 lines) with class distribution, gender, intensity, speech-vs-song analysis, waveform comparisons, and emotion-class spectrogram visualizations.
- Completed **data preprocessing notebook** (`03-data-preprocessing.ipynb`, +538 lines) for audio trimming, silence removal, amplitude normalization, and padding.
- Created **`src/utils/eda.py`** (15 lines) — reusable EDA plotting utilities.
- Created **`src/utils/data_preprocessing.py`** (115 lines) — audio trimming, normalization, and padding functions.
- Generated **7 figures** saved to `docs/02-results/figures/`: emotion distribution, gender distribution, intensity distribution, speech vs. song, spectrogram analysis, waveform comparison, and multi-emotion spectrograms.
- **Khaled** contributed:
  - Rewrote **data acquisition notebook** (`01-data-acquisition.ipynb`, +951 lines) with full download and speaker-disjoint split logic.
  - Completed **feature engineering notebook** (`04-feature-engineering.ipynb`, +819 lines) for mel spectrogram and MFCC feature extraction.
  - Created `src/utils/data_acquisition.py` (88 lines) and updated `src/utils/feature_engineering.py` (+210 lines) with reusable extraction functions.
  - Generated `split_labels.csv` with per-file label mappings for the full dataset.
  - Added 2 figures: `fig04-data_augmentation.png` and `fig04-mel_spectrogram.png`.
- Multiple refinement iterations on notebooks and documentation.

### Results Achieved

| Metric | CNN1D | MFCC+SVM |
|--------|-------|----------|
| **Val accuracy** (speakers 20–22) | **75.38%** | 62.88% |
| **Test accuracy** (speakers 23–24) | 66.48% | **70.45%** |
| Parameters | 132,806 | N/A (SVM) |
| Disk size | ~530 KB | ~3 MB |
| CPU latency (mean) | ~0.53 ms | ~0.20 ms |
| Optimizer / Scheduler | AdamW + OneCycleLR | GridSearchCV (5-fold) |
| Regularization | Dropout 0.3, Label Smoothing 0.05, SpecAugment | RBF kernel, C=1.0 |

### Key Decisions

- **SpecAugment** applied only during training (time masking: max 30 frames, freq masking: max 12 bands, 2 masks each) — improves generalization without changing the model architecture.
- **AdamW + OneCycleLR** chosen over Adam + ReduceLROnPlateau — OneCycleLR's warmup+annealing schedule empirically converges faster for this task.
- **Early stopping** patience set to 10 epochs on val loss to prevent overfitting.
- **Label smoothing** (0.05) used to soften target distributions — particularly important given emotion class ambiguities (e.g., calm vs. sad).
- SVM parameter grid deliberately kept small (RBF/linear/poly, C in {0.1, 1, 10}) to keep grid search tractable on CPU.

### Issues Encountered

- **CNN underperforms SVM on held-out test set** (66.48% vs. 70.45%) despite dominating on validation (75.38% vs. 62.88%). Likely causes:
  1. Small test set (176 samples, 2 speakers) → high variance in metrics.
  2. SVM with RBF kernel may generalize better on very small datasets.
  3. Potential overfitting to val set characteristics during early stopping.
- **"happy" class is hardest for both models**: CNN achieves only 46.88% test accuracy on happy; SVM 62.50%. Happy is frequently confused with fearful/calm — these emotions share similar prosodic patterns in acted speech.
- **Filename typo**: `data_acquistion.py` (missing 'i') — left as-is to avoid breaking notebook references across the pipeline.
- **Midterm report filename**: renamed from `Midterm_Group(10)` to `midterm-group` for cleaner paths, committed as a file move (Git detected as rename).

### Relevant Commits

| Commit | Author | Description |
|--------|--------|-------------|
| `caa4366` | Elsayed Elmandoh | Midterm report upload + workflow diagrams |
| `6301d64` | Elsayed Elmandoh | Pipeline refactor: feature_engineering.py, data_acquisition rename |
| `79af6b3` | Elsayed Elmandoh | Config refactor to Pydantic; midterm report rename + figures |
| `12517bf` | Elsayed Elmandoh | First pipeline execution: CSV artifacts, feature arrays |
| `eb5bbca` | Elsayed Elmandoh | **Major**: full training + eval results, models, tests, pyproject, README |
| `1c07cbd` | Elsayed Elmandoh | cnn1d_model.py + svm_model.py implementation |
| `7112d2d` | Elsayed Elmandoh | Training curves figure added to docs |
| `f7bdc9a` | Salma Abdelfattah | Completed EDA notebook + preprocessing utilities |
| `08b1e67` | Khaled Ashoush | Uploaded training/evaluation/testing notebooks |
| `f351da2` | Khaled Ashoush | Uploaded preprocessing notebook |

---

## Week 4 — Finalization & Final Report (June 7–8, 2026)

### Progress

- **Merged `final-report` branch into `main`** — resolved `app.py` conflict between independent changes on both branches.
- **Generated held-out test set predictions** for both models (speakers 23–24, 176 samples):
  - CNN1D: 66.48% accuracy
  - MFCC+SVM: 70.45% accuracy
- **Finalized documentation**: README reviewed and polished across multiple passes (formatting fixes, badge alignment, results summary).
- **Refined `.gitignore`** to exclude large data artifacts, model checkpoints, and IDE files.
- **Final report directory structure** and presentation outline finalized.
- **Comparison analysis notebook** (`08-comparision/00-quickstart.ipynb`) created as entry point for final model comparison results.

### Final Results Summary

| Split | Samples | Speakers | SVM Accuracy | CNN Accuracy |
|-------|---------|----------|-------------|-------------|
| Validation | 264 | 20, 21, 22 | 62.88% | **75.38%** |
| Test | 176 | 23, 24 | **70.45%** | 66.48% |

**Best per-class performance (test set):**
- SVM excels on: fearful (90.62%), calm (81.25%)
- CNN excels on: angry (84.38%), sad (75.00%)
- Both struggle with: neutral (50%), happy (46.88%–62.50%)

### Key Decisions

- **No further hyperparameter tuning** — the CNN's validation accuracy (75.38%) was competitive with published lightweight SER results on RAVDESS, and further tuning risked overfitting to the small val set.
- **Final deliverable structure**: code + README + reproducible notebooks + model checkpoints + prediction JSONs, per the project requirements.

### Issues Encountered

- **Test set size (176 samples, 2 speakers)** is a known limitation — confidence intervals on test metrics are wide (±5–7%). Any single-number comparison between models should be treated as suggestive, not conclusive.
- **`app.py` merge conflict** between `final-report` branch and `main` — resolved by keeping the final version from `final-report` which included the Streamlit app with trained model loading.
- **Cross-channel analysis** deferred — speech 6-class comparison is the primary result. Song-channel and cross-channel experiments are structured in the codebase but results not yet generated.

### Relevant Commits

| Commit | Author | Description |
|--------|--------|-------------|
| `d531daa` | Elsayed Elmandoh | Merge `final-report` → `main`; resolved app.py conflict |
| `004b269` | Elsayed Elmandoh | Post-merge updates |
| `3700612` | Elsayed Elmandoh | Final repo state: all results, docs, and code |
| `0a11ce0` | Khaled Ashoush | Final notebook uploads |
| `1a7fbbf` | Elsayed Elmandoh | `.gitignore` final refinements |

---

## Notes on Commit Message Quality

Many commits throughout this project use the generic message `"update"`, which does not describe the actual changes made. For future projects, we recommend:

1. **Descriptive commit messages**: e.g., `"feat: add SpecAugment to MelSpectrogramDataset"` instead of `"update"`.
2. **Conventional Commits format** (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`) for automated changelog generation.
3. **LOG.md updates as part of each work session** rather than retroactively — entries should be written alongside commits, not reconstructed from git history.

Despite the vague messages, the substantive work done in each phase is clearly visible through the file diffs and accumulated changes.
