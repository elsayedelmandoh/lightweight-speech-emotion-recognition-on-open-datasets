# 02 - data & method

## slide 5: ravdess dataset
- 24 north american english actors (12 male, 12 female)
- speech + song, 2 statements each, normal/strong intensity
- full: 7356 files, 8 emotions
- our 6-class subset: neutral, calm, happy, sad, angry, fearful (drop disgust, surprise)
- 1628 train / 264 val / 176 test
- neutral under-represented (~188 vs ~376 per other emotion)

<img src="../../02-results/figures/fig02-emotion-distribution.png" width="500">
*fig a. emotion distribution — neutral bar is ~half the height of others (~188 vs ~376)*

<img src="../../02-results/figures/fig02-gender-distribution.png" width="500">
*fig b. gender distribution — 12 male, 12 female actors, roughly balanced*

## slide 6: speaker-disjoint split
- train: actors 1-19 (1628 samples)
- val: actors 20-22 (264 samples)
- test: actors 23-24 (176 samples)
- no speaker overlap between splits -- measures true cross-speaker generalization

<img src="../../02-results/figures/fig02-intensity-distribution.png" width="500">
*fig c. intensity distribution — normal vs strong bars are close in height, balanced split*

<img src="../../02-results/figures/fig02-speech-vs-song.png" width="500">
*fig d. speech vs song — speech slice is ~59%, song ~41%, we fuse both channels*

## slide 7: preprocessing
- resample 16khz mono, trim/pad 4s (64000 samples)
- silence trimming (-25db threshold), pre-emphasis (0.97), rms normalization
- for cnn: 128-band log-mel-spectrogram, 251 frames, per-sample normalized
- for svm: 40 mfcc + delta + delta-delta, mean+std pooled -> 240-dim vector

<img src="../../02-results/figures/fig03-waveform_comparison.png" width="600">
*fig e. waveform comparison — original vs processed: 16khz, 4s, normalized amplitude*

<img src="../../02-results/figures/fig03-emotions_spectrograms.png" width="600">
*fig f. sample spectrograms — 6 panels, one spectrogram per emotion, shows distinguishable acoustic patterns*

<img src="../../02-results/figures/fig03-spectrogram_analysis.png" width="600">
*fig g. spectrogram analysis — 3-panel: waveform, spectrogram, log-mel spectrogram for one sample*

## slide 8: feature extraction & augmentation
- log-mel: 128 bands, 1024-pt fft, 256-sample hop, 251 frames
- mfcc: 40 coeffs + delta + delta-delta, pooled -> 240-dim
- specaugment: time mask 30, freq mask 12, n=2 (during cnn training only)

<img src="../../02-results/figures/fig04-mel_spectrogram.png" width="500">
*fig h. mel-spectrogram — 128 mel bands x 251 time frames, the cnn input*

<img src="../../02-results/figures/fig04-data_augmentation.png" width="600">
*fig i. augmentation demo — original waveform + 3 augmented versions (noise, pitch shift, time stretch)*

## slide 9: svm baseline
- standardscaler on 240-dim mfcc features
- 5-fold grouped cv grid search (15 combos x 5 folds = 75 fits)
- kernels: rbf, linear, polynomial degree 2
- key finding: initial c in {0.1, 1, 10, 50} overfit (100% train, 65% test)
- capping c at {0.1, 1} reduced gap 35pp -> 24pp, test accuracy 65% -> 70.45%
- final: rbf kernel, c=1.0, gamma="scale", probability=true
- training: ~2 min on cpu

| parameter | value |
|-----------|-------|
| feature scaler | standardscaler |
| kernel | rbf |
| c | 1.0 |
| gamma | "scale" |
| probability | true |
| cv folds | 5 (grouped by actor) |
| grid size | 15 combos x 5 folds = 75 fits |

*table a. svm baseline hyperparameters*

## slide 10: 1d cnn architecture
- input: (128, 251) log-mel-spectrogram
- conv1d(128->64, k=5) + bn + relu + maxpool(2)
- conv1d(64->128, k=5) + bn + relu + maxpool(2)
- conv1d(128->128, k=3) + bn + relu + adaptiveavgpool(1)
- dropout(0.3) + linear(128, 6)
- 132,806 parameters (~528 kb on disk)

## slide 11: cnn training
- loss: cross-entropy with label smoothing 0.05
- optimizer: adamw (lr=1e-3, weight_decay=5e-4)
- scheduler: onecyclelr (max_lr=3e-3, 5-epoch warmup)
- batch size: 32, epochs: 80 (early stopping patience 20)
- device: gpu for training (~47 s for 80 epochs), cpu for inference
- specaugment during training only

| parameter | value |
|-----------|-------|
| optimizer | adamw |
| learning rate (peak) | 3e-3 (onecyclelr) |
| weight decay | 5e-4 |
| batch size | 32 |
| epochs | 80 (early stopping, patience 20) |
| loss | cross-entropy + label smoothing 0.05 |
| specaugment | time mask=30, freq mask=12, n=2 |
| dropout | 0.3 |
| parameters | 132,806 |

*table b. 1d cnn training hyperparameters*

## slide 12: evaluation protocol
- metrics: train/val/test accuracy, per-class recall, confusion matrix, cpu latency
- test set held out from all training + hyperparameter selection
- latency: average 50 (svm) or 200 (cnn) inference calls after 5-call warmup
