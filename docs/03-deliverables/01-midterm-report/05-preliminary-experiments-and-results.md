# preliminary experiments and results

## current status

as of the midterm checkpoint, we have completed data acquisition, exploratory data analysis, preprocessing, and an initial mfcc + svm baseline run on a representative sample subset (416 files, 17% of the full dataset). full-scale model training is planned as the next phase.

## completed work

### 1. data acquisition

- downloaded ravdess audio-only files (2452 total: 1440 speech + 1012 song) from zenodo.
- verified file integrity: all files present and readable across 47 actor directories.
- parsed filename metadata into structured labels (emotion, intensity, statement, repetition, actor, gender).
- created speaker-disjoint split: train actors 01-19 (1932 files), val 20-22 (312), test 23-24 (208).
- exported `data/processed/split_labels.csv` for downstream notebooks.
- created sample subset in `data/samples/` (4 actors, 416 files) for rapid iteration.

### 2. exploratory data analysis

analysis of the full dataset revealed:

- **class distribution**: balanced for all emotions except neutral (96 files vs 192) due to missing strong-intensity variant.
- **clip durations**: most clips are 3-5 seconds long. statement-based timing variation is minimal.
- **waveform characteristics**: high-arousal emotions (angry, fearful, surprised) show greater amplitude and wider dynamic range compared to low-arousal emotions (sad, calm, neutral).
- **mel spectrograms**: distinct frequency patterns across emotions. high-arousal emotions exhibit broader frequency bandwidth, particularly in the 0-4khz range.

### 3. preprocessing pipeline

- silence trimming using decibel threshold (top_db=20) removes 0.5-1.5s per clip.
- amplitude normalization to [-1, 1].
- fixed-length padding/truncation to 3 seconds (144000 samples at 48khz).
- pipeline verified end-to-end on all sample files without errors.

### 4. mfcc + svm baseline (preliminary)

run on the sample subset (208 train clips from actors 01-02, 104 test clips from held-out actor 23):

| metric | value |
|--------|-------|
| test accuracy | 27.9% |
| macro f1 | 0.238 |
| feature extraction time | 17.0s (0.082s per clip) |
| training time | 0.04s |
| inference latency | 0.59ms per clip (single) |
| model size | 412 kb |

the low accuracy is expected: training on only 2 actors and testing on an unseen speaker is the hardest evaluation setting. the baseline shows the model is learning (27.9% vs 12.5% random chance for 8-class) but requires more training speakers to generalize.

the confusion matrix shows the model struggles most with low-arousal emotions (sad, calm, disgust) while achieving better results on high-arousal categories (happy, angry, fearful).

## implementation details

- **language**: python 3.12.13
- **key libraries**: librosa 0.11.0 (audio loading, mfcc extraction), scikit-learn 1.8.0 (svm, metrics, scaling), numpy, pandas, matplotlib, seaborn, joblib
- **environment**: conda on wsl2 (ubuntu), jupyter notebooks
- **hardware**: cpu-based development (intel x86_64)
- **version control**: git repository with numbered notebook pipeline
- **sample data**: 416 wav files in `data/samples/`, with `sample_labels.csv`

## next steps

1. scale feature extraction to the full dataset (2452 clips).
2. train svm with grid search on full training set (19 actors, 1932 files).
3. implement and train 1d cnn on log-mel spectrograms.
4. evaluate on held-out test actors with confusion matrix and per-speaker analysis.
5. run cross-channel experiments (speech to song, song to speech).
