# end-to-end workflow and handoff points

## pipeline phases

| phase | notebook | input | output | handoff |
|-------|----------|-------|--------|---------|
| 1. data acquisition | `01-data-acquisition/` | ravdess urls | `data/raw/` wav files | raw files on disk |
| 2. eda | `02-eda/` | `data/raw/` | distribution plots, label counts | understanding of class balance, clip lengths |
| 3. preprocessing | `03-data-preprocessing/` | `data/raw/` | `data/processed/` cleaned wavs | trimmed, normalized audio |
| 4. feature engineering | `04-feature-engineering/` | `data/processed/` | mel spectrograms + mfccs as .npy | feature arrays + train/val/test splits |
| 5. model training | `05-model-training/` | feature arrays | `data/models/` checkpoints | trained cnn + svm models |
| 6. model evaluation | `06-model-evaluation/` | models + test set | metrics, confusion matrices | performance comparison tables |
| 7. model testing | `07-model-testing/` | held-out test | final results, error analysis | deliverable-ready outputs |

## execution order

notebooks must run in numbered sequence. each phase depends on the output of the previous one. skipping a phase will cause missing file errors in downstream notebooks.

## verification at each handoff

1. **acquisition -> eda**: verify file count matches expected (1440 speech files for ravdess).
2. **eda -> preprocessing**: confirm no corrupted files, all clips readable.
3. **preprocessing -> features**: confirm output shapes (n_clips x n_mels x time_frames).
4. **features -> training**: confirm train/val/test splits are speaker-disjoint and stratified.
5. **training -> evaluation**: model checkpoint loads and produces predictions without errors.
6. **evaluation -> testing**: metrics are reasonable (not random-chance level).
