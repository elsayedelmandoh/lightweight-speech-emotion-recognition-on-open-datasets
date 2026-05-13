# solution overview and approach

## what we will build

a lightweight 1d cnn that classifies emotions from speech and song audio using mel spectrograms as input, compared against an mfcc + svm baseline across multiple scenarios (speech-only 8-class, song-only 6-class, combined 8-class, cross-channel). the system targets cpu inference with minimal latency.

## approach

### 1. data pipeline (completed)
- ravdess audio-only files downloaded to `data/raw/`.
- emotion labels parsed from 7-part filename convention (see 05-dataset.md).
- speaker-disjoint split applied: train (actors 01-19), val (20-22), test (23-24).
- data organized: `data/{train,val,test}/{speech,song}/Actor_XX/`.
- **2452 files total** (1440 speech + 1012 song).

### 2. preprocessing
- load wav files (16-bit, 48khz, mono) from the split directory structure.
- trim silence (top_db=20), amplitude normalize to [-1, 1].
- pad/truncate to fixed length (3 seconds = 144000 samples at 48khz).
- output cleaned wavs or load directly for feature extraction.

### 3. feature extraction
- **for cnn**: compute log-mel spectrogram (n_mels=128, n_fft=2048, hop_length=512).
  - output shape per clip: (128, ~282). transpose to (282, 128) for 1d cnn (time = sequence, mel = channels).
- **for svm**: extract 40 mfccs + delta + delta-delta, aggregate mean+std per clip (240-dim vector).

### 4. baseline model (mfcc + svm)
- input: 240-dim mfcc feature vector.
- svm with rbf kernel, grid search c and gamma.
- trained and evaluated on same speaker-disjoint splits as cnn.
- **three baseline variants**: speech-only 8-class, song-only 6-class, combined.

### 5. cnn model
- input: mel spectrogram (time_frames x n_mels), 1d sequence with mel bands as channels.
- architecture:
  - 3 conv1d blocks: 64 -> 128 -> 256 channels, kernel=5, padding=same
  - each block: conv1d -> batchnorm -> relu -> maxpool(2) -> dropout(0.25)
  - global average pooling -> fc(256->128) -> relu -> dropout(0.5) -> fc(128->n_classes)
  - ~200k parameters, ~1mb.
- training: cross-entropy loss, adam (lr=1e-3), cosine annealing, batch_size=32, early stopping.
- regularization: dropout, weight decay (1e-4).
- **three training scenarios**: speech-only (8-class), song-only (6-class), combined (8-class).

### 6. evaluation
- metrics: accuracy, per-class f1, macro-f1, weighted-f1, confusion matrix.
- compare cnn vs svm on all three scenarios.
- cross-channel: train on speech, test on song (and vice versa).
- cross-speaker: per-actor accuracy on held-out speakers 22-24.
- inference benchmark: latency (ms/clip on cpu), model size (mb).

### 7. deployment
- export best model as torchscript for cpu inference.
- optional: huggingface spaces demo with gradio interface.
