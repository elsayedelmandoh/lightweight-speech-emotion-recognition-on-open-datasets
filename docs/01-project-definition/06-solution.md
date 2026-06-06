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
- **for cnn**: compute log-mel spectrogram (n_mels=128, n_fft=1024, hop_length=256).
  - output shape per clip: (128, ~251) for 4s at 16khz. the 1d cnn receives (batch, 128, 251) with mel bands as channels and time as the conv dimension.
- **for svm**: extract 40 mfccs + delta + delta-delta, aggregate mean+std per clip (240-dim vector).

### 4. baseline model (mfcc + svm)
- input: 240-dim mfcc feature vector.
- svm with rbf kernel, grid search c and gamma.
- trained and evaluated on same speaker-disjoint splits as cnn.
- **three baseline variants**: speech-only 8-class, song-only 6-class, combined.

### 5. cnn model
- input: mel spectrogram (time_frames x n_mels), 1d sequence with mel bands as channels.
- architecture:
  - 3 conv1d blocks: 128 -> 64 -> 128 -> 128 channels, kernel=5/5/3, padding=2/2/1
  - each block: conv1d -> batchnorm -> relu -> maxpool(2) (third block uses adaptiveavgpool(1) instead of maxpool)
  - classifier: dropout(0.3) -> linear(128, n_classes)
  - ~133k parameters, <600 kb.
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
