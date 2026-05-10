# research notes and observations

## dataset selection

- **ravdess**: smaller, easier to start with. professional actors (acted) - higher performance but less realistic generalization. 1440 speech files across 24 actors.
- **crema-d**: larger and more diverse. harder, more realistic speaker variation.
- recommendation: start with ravdess. if time allows, run additional experiments on crema-d for cross-dataset validation.

## mfcc (mel-frequency cepstral coefficients)

- widely used feature extraction for audio and speech tasks.
- represents the short-term power spectrum of a sound in a compact form that mimics human hearing.
- standard for classical ser baselines (svm, knn, random forest).
- typical config: 13-40 coefficients per frame, with delta and delta-delta features.

## mel spectrogram vs mfcc

- mel spectrograms retain more frequency information than mfccs (which apply dct compression).
- cnns on mel spectrograms generally outperform mfcc-based pipelines (neumann & vu 2017).
- for 1d cnn: feed mel spectrogram as time x frequency matrix directly.

## 1d cnn vs 2d cnn for ser

- 2d cnn treats spectrogram as image (time x frequency). higher accuracy but more parameters.
- 1d cnn operates along the time axis with frequency bands as channels. fewer parameters, faster inference.
- 1d cnn is better suited for cpu/edge deployment.

## cross-speaker evaluation

- ravdess has 24 identified actors. use speaker-disjoint train/test splits to measure generalization.
- leave-one-speaker-out or group split (e.g., train on actors 1-18, test on 19-24).
- actor id is encoded in filename (odd = male, even = female).
