# system architecture and component boundaries

## pipeline overview

```
raw audio (wav)
    |
    v
[preprocessing]  -- silence trim, normalize, pad/truncate to 3s
    |
    v
[feature extraction]  -- mel spectrogram (cnn) / mfcc (svm)
    |
    v
[model inference]  -- 1d cnn or svm
    |
    v
[predicted emotion]
```

## data layout (current)

```
data/
  train/speech/Actor_01..19/   (1140 files)
  train/song/Actor_01..17,19/  (792 files)
  val/speech/Actor_20,21,22/   (180 files)
  val/song/Actor_20,21,22/     (132 files)
  test/speech/Actor_23,24/     (120 files)
  test/song/Actor_23,24/       (88 files)
```

data is already speaker-disjoint split, no further splitting needed.

## components

### preprocessing (`notebooks/03-data-preprocessing/`)
- input: wav files from `data/{train,val,test}/{speech,song}/Actor_XX/`
- output: cleaned wav arrays (or load directly for feature extraction)
- responsibilities: silence trimming, amplitude normalization, fixed-length padding/truncation

### feature extraction (`notebooks/04-feature-engineering/`)
- input: cleaned wav arrays + split metadata
- output: feature arrays saved as .npy in `data/processed/`
- for cnn: log-mel spectrograms, shape (n_clips, time_frames, n_mels)
- for svm: mfcc + delta + delta-delta aggregates, shape (n_clips, 240)
- also saves label arrays (emotion class ints)

### model training (`notebooks/05-model-training/`)
- input: feature arrays + labels from `data/processed/`
- output: trained model artifacts in `data/models/`
- responsibilities: define 1d cnn architecture, train, validate, save checkpoints (.pt, .pt scripted)
- three training scenarios: speech-only, song-only, combined

### model evaluation (`notebooks/06-model-evaluation/`)
- input: trained model + test features
- output: metrics, plots, confusion matrices in `data/predictions/` and `docs/02-results/`
- responsibilities: accuracy, f1, confusion matrix, latency benchmark, model size
- cross-speaker analysis: per-actor accuracy on held-out speakers

### model testing (`notebooks/07-model-testing/`)
- input: held-out test set
- output: final results, comparison tables
- responsibilities: cnn vs svm comparison, cross-channel (speech<->song), error analysis

### configuration (`src/config/settings.py`)
- central location for hyperparameters, paths, feature dimensions
- all notebooks import from here (once populated)

### shared utilities (`src/utils/helpers.py`)
- common functions: data loading, label parsing from filename, visualization helpers
- all notebooks import from here (once populated)

## data flow

```
data/{train,val,test}/{speech,song}/  -->  data/processed/  -->  data/models/  -->  data/predictions/
        |                                      |                    |                   |
   wavs by split                          mel/mfcc npy        .pt checkpoints     prediction csvs
```

## cnn architecture (specific)

```
input: (batch, time_frames=282, n_mels=128)
  |
conv1d(128->64, k=5, padding=same) -> batchnorm -> relu -> maxpool(2) -> dropout(0.25)
  |
conv1d(64->128, k=5, padding=same) -> batchnorm -> relu -> maxpool(2) -> dropout(0.25)
  |
conv1d(128->256, k=3, padding=same) -> batchnorm -> relu -> maxpool(2) -> dropout(0.25)
  |
global avg pooling (1d) -> fc(256->128) -> relu -> dropout(0.5)
  |
fc(128->n_classes)  # 8 for speech/combined, 6 for song-only
```

~200k parameters, ~1mb model size.

## failure points

- feature extraction is compute-intensive for 2452 files. caching to disk (.npy) is essential.
- speaker-disjoint splits already enforced. must not accidentally merge splits during loading.
- model training may overfit on small dataset (especially speech-only 1440 files). regularization (dropout, weight decay) and early stopping required.
- song data has only 6 classes. when training combined 8-class, song contributes zero samples for disgust and surprised -- class imbalance must be handled.
