# methodology

## data description

### dataset: ravdess

we use the ryerson audio-visual database of emotional speech and song (ravdess) [1], specifically the audio-only speech and song portions. key characteristics:

- **files**: 2452 wav files (1440 speech + 1012 song), 16-bit, 48khz, mono
- **actors**: 24 professional actors (12 female, 12 male). actor 18 has no song files
- **speech emotions**: 8 classes - neutral, calm, happy, sad, angry, fearful, disgust, surprised
- **song emotions**: 6 classes - neutral, calm, happy, sad, angry, fearful
- **intensity**: 2 levels per emotion (normal, strong), except neutral

filenames encode metadata as 7 hyphen-separated integers: modality-vocal_channel-emotion-intensity-statement-repetition-actor. for example, 03-01-06-01-02-01-12.wav is audio-only speech, fearful, normal intensity, statement 2, 1st repetition, actor 12 (female).

### train/validation/test split

we use a speaker-disjoint split to evaluate cross-speaker generalization:

| split | actors | speech files | song files | total |
|-------|--------|-------------|------------|-------|
| train | 01-19 | 1140 | 792 | 1932 |
| validation | 20-22 | 180 | 132 | 312 |
| test | 23-24 | 120 | 88 | 208 |

## preprocessing

1. load audio via librosa at 48khz.
2. silence trimming (top_db=20).
3. amplitude normalization to [-1, 1].
4. padding/truncation to 3 seconds (144000 samples).

## feature extraction

### log-mel spectrogram (cnn input)

- stft: 25ms window, 10ms hop (n_fft=2048, hop_length=512).
- 128 mel bands (fmin=0, fmax=8000).
- log scale: log_mel = log(mel + 1e-9).
- shape per clip: (128, ~282). transposed to (282, 128) for 1d cnn.

### mfcc (svm baseline input)

- 40 mfcc coefficients per frame.
- delta + delta-delta features.
- mean + std per clip: 240-dim vector.

## training scenarios

| scenario | channel | classes | train files |
|----------|---------|---------|-------------|
| speech-only | speech | 8 | 1140 |
| song-only | song | 6 | 792 |
| combined | both | 8 | 1932 |

cross-channel: train on speech test on song and vice versa.

## model architectures

### 1d cnn

input (282, 128) -> conv1d(128->64, k=5) -> bn -> relu -> pool(2) -> drop(0.25) -> conv1d(64->128, k=5) -> bn -> relu -> pool(2) -> drop(0.25) -> conv1d(128->256, k=3) -> bn -> relu -> pool(2) -> drop(0.25) -> global avg pool -> fc(256->128) -> relu -> drop(0.5) -> fc(128->n_classes)

~200k params, ~1mb.

### svm baseline

rbf kernel, 240-dim mfcc input. grid search c=[0.1,1,10,100], gamma=['scale','auto',0.01,0.001].

## training config

| parameter | value |
|-----------|-------|
| optimizer | adam |
| lr | 1e-3 (cosine annealing) |
| batch size | 32 |
| max epochs | 100 (early stopping patience=15) |
| loss | cross-entropy |
| regularization | dropout 0.25-0.5, weight decay 1e-4 |

## evaluation metrics

accuracy, macro f1, per-class precision/recall/f1, confusion matrix, per-speaker accuracy, inference latency (ms on cpu), model size (mb).
