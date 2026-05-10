# solution overview and approach

## what we will build

a lightweight 1d cnn that classifies emotions from speech audio using mel spectrograms as input, compared against an mfcc + svm baseline. the system targets cpu inference with minimal latency.

## approach

### 1. data pipeline
- download ravdess audio-only speech files.
- parse emotion labels from filename convention (see 05-dataset.md).
- split by speaker (not random) to evaluate cross-speaker generalization.

### 2. preprocessing
- load wav files (16-bit, 48khz).
- trim silence, normalize amplitude.
- extract log-mel spectrograms (target: 128 mel bands, ~2s windows).
- optionally extract mfccs (40 coefficients) for the baseline.

### 3. baseline model
- extract mfcc statistics (mean, std, delta) per clip.
- train svm (rbf kernel) with grid-search hyperparameter tuning.
- evaluate on same speaker-disjoint test split.

### 4. cnn model
- input: mel spectrogram (time x n_mels), treated as 1d sequence with mel bands as channels.
- architecture: 3-4 conv1d blocks (conv + batchnorm + relu + maxpool) -> global avg pool -> fc -> softmax.
- training: cross-entropy loss, adam optimizer, learning rate scheduling.
- regularization: dropout, weight decay.

### 5. evaluation
- metrics: accuracy, per-class f1, confusion matrix.
- compare cnn vs svm baseline on same test split.
- measure inference latency and model size.
- analyze errors by emotion, speaker gender, and intensity.

### 6. deployment
- export model as torchscript for cpu inference.
- optional: huggingface spaces demo with gradio interface.
