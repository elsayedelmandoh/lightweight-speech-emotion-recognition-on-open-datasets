# research notes and observations

## dataset selection

- **ravdess**: smaller, easier to start with. professional actors (acted) - higher performance but less realistic generalization. 2452 audio-only files (1440 speech + 1012 song) across 24 actors.
- **crema-d**: larger and more diverse. harder, more realistic speaker variation.
- recommendation: start with ravdess. if time allows, run additional experiments on crema-d for cross-dataset validation.

## actual data split (implemented)

speaker-disjoint split by actor id:

| split | speech actors | speech files | song actors | song files | total |
|-------|--------------|-------------|------------|-----------|-------|
| train | 01-19 | 1140 | 01-17, 19 | 792 | 1932 |
| val | 20-22 | 180 | 20-22 | 132 | 312 |
| test | 23-24 | 120 | 23-24 | 88 | 208 |

location: `data/{train,val,test}/{speech,song}/Actor_XX/*.wav`

## mfcc (mel-frequency cepstral coefficients)

- widely used feature extraction for audio and speech tasks.
- represents the short-term power spectrum of a sound in a compact form that mimics human hearing.
- standard for classical ser baselines (svm, knn, random forest).
- typical config: 13-40 coefficients per frame, with delta and delta-delta features.

## mel spectrogram vs mfcc

- mel spectrograms retain more frequency information than mfccs (which apply dct compression).
- cnns on mel spectrograms generally outperform mfcc-based pipelines (neumann & vu 2017).
- for 1d cnn: feed mel spectrogram as time x frequency matrix directly (time = sequence dim, mel bands = channels).

## 1d cnn vs 2d cnn for ser

- 2d cnn treats spectrogram as image (time x frequency). higher accuracy but more parameters.
- 1d cnn operates along the time axis with frequency bands as channels. fewer parameters, faster inference.
- 1d cnn is better suited for cpu/edge deployment.

## speech vs song differences

- speech (8 emotions): calm, happy, sad, angry, fearful, disgust, surprised + neutral
- song (6 emotions): same minus disgust and surprised
- song is more melodic and sustained. emotions may express differently in singing than speech.
- cross-channel testing (train on speech, test on song and vice versa) tests how well the model learns emotion vs channel-specific acoustic features.

## cross-speaker evaluation

- ravdess has 24 identified actors. use speaker-disjoint train/test splits to measure generalization.
- our split: train actors 01-19, val 20-22, test 23-24.
- actor id is encoded in filename (odd = male, even = female).
