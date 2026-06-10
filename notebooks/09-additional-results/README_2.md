# Speech Emotion Recognition Benchmark

A publication-oriented Speech Emotion Recognition (SER) benchmark project comparing classical machine learning, deep learning, transfer learning, and self-supervised learning approaches under a strict speaker-independent evaluation protocol.

---

## Project Goal

The objective is to compare multiple architectures on the same dataset and preprocessing pipeline to determine which model performs best for Speech Emotion Recognition.

Models included:

| Category | Model |
|-----------|-----------|
| Classical ML | SVM |
| Deep Learning (1D) | CNN1D + Attention + BiLSTM |
| Deep Learning (2D) | CNN2D + Attention + BiLSTM |
| Transfer Learning | PANNs |
| Self-Supervised Learning | Wav2Vec2 |

---

## Datasets

### RAVDESS

- Speech recordings only
- Song recordings removed
- 24 actors
- 1440 samples

Used emotions:

- Angry
- Disgust
- Fearful
- Happy
- Neutral
- Sad

Removed:

- Calm
- Surprised

---

### CREMA-D

- 7442 samples
- 91 actors

Used emotions:

- Angry
- Disgust
- Fearful
- Happy
- Neutral
- Sad

---

## Final Merged Dataset

| Dataset | Samples |
|----------|----------|
| RAVDESS | 1056 |
| CREMA-D | 7442 |
| Total | 8498 |

Total Speakers:

115

---

## Emotion Labels

| Emotion | Label |
|----------|----------|
| Angry | 0 |
| Disgust | 1 |
| Fearful | 2 |
| Happy | 3 |
| Neutral | 4 |
| Sad | 5 |

---

## Audio Preprocessing

A unified preprocessing pipeline is applied to all files:

```text
Load
→ Mono
→ Resample
→ Silence Trimming
→ RMS Normalization
→ Pad / Truncate