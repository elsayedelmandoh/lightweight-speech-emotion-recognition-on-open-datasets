# system architecture and component boundaries

## pipeline overview

```
raw audio (wav)
    |
    v
[preprocessing]  -- trim, normalize, resample
    |
    v
[feature extraction]  -- mel spectrogram / mfcc
    |
    v
[model inference]  -- 1d cnn or svm
    |
    v
[predicted emotion]
```

## components

### preprocessing (`notebooks/03-data-preprocessing/`)
- input: raw wav files from `data/raw/`
- output: cleaned wav files in `data/processed/`
- responsibilities: silence trimming, amplitude normalization, resampling if needed

### feature extraction (`notebooks/04-feature-engineering/`)
- input: processed wav files
- output: mel spectrograms and mfcc features saved as numpy arrays in `data/processed/`
- responsibilities: compute log-mel spectrograms, mfccs, delta features, split into train/val/test

### model training (`notebooks/05-model-training/`)
- input: feature arrays + labels
- output: trained model artifacts in `data/models/`
- responsibilities: define cnn architecture, train, validate, save checkpoints

### model evaluation (`notebooks/06-model-evaluation/`)
- input: trained model + test features
- output: metrics, plots, confusion matrices in `data/predictions/` and `docs/02-results/`
- responsibilities: accuracy, f1, confusion matrix, latency benchmark, model size

### model testing (`notebooks/07-model-testing/`)
- input: held-out test set
- output: final results and comparison table
- responsibilities: cross-speaker analysis, cnn vs svm comparison, error analysis

### configuration (`src/config/settings.py`)
- central location for hyperparameters, paths, feature dimensions
- all notebooks import from here (once populated)

### shared utilities (`src/utils/helpers.py`)
- common functions: data loading, label parsing, visualization helpers
- all notebooks import from here (once populated)

## data flow

```
data/raw/  -->  data/processed/  -->  data/models/  -->  data/predictions/
   |                |                    |                   |
ravdess wavs    mel/mfcc npy        .pt checkpoints     prediction csvs
```

## failure points

- feature extraction is the most compute-intensive step. caching to disk is essential.
- speaker-disjoint splits must be enforced strictly to avoid data leakage.
- model training may overfit on small dataset. regularization and early stopping required.
