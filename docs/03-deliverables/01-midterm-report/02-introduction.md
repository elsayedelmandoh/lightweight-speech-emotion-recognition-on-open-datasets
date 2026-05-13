# introduction

## problem statement

human speech carries rich paralinguistic information beyond lexical content; prosody, rhythm, and spectral characteristics encode a speaker's emotional state in ways that are both computationally accessible and practically valuable. robust emotion recognition from speech remains an open problem, complicated by speaker variability, cultural differences in expression, and the inherent ambiguity of affective labels.

the core tension in ser is between accuracy and efficiency. classical methods such as mfcc features with svm classifiers are lightweight but achieve modest accuracy on ravdess (50-65%) because they fail to capture the temporal and spectral dynamics of emotional speech. conversely, deep learning models including 2d cnns achieve higher accuracy but are often over-parameterized for the task, making deployment on cpu-only environments impractical.

## motivation

there is a clear need for ser models that occupy the middle ground: architectures that leverage the pattern-recognition capabilities of convolutional networks while remaining small enough for cpu inference. 1d cnns offer a promising direction because they operate directly on the time axis of mel spectrograms with frequency bands as input channels, requiring far fewer parameters than 2d cnns that treat spectrograms as images [1]. additionally, the ravdess dataset includes both speech and song recordings, enabling investigation of cross-channel generalization - a relatively underexplored question in ser literature.

## project scope

this project focuses on:

- implementing a 1d cnn for emotion classification on ravdess across three scenarios: speech-only (8-class, 1440 files), song-only (6-class, 1012 files), and combined (8-class, 2452 files)
- building an mfcc + svm baseline for direct comparison on all scenarios
- evaluating cross-speaker generalization using speaker-disjoint train/val/test splits (train: actors 01-19, val: 20-22, test: 23-24)
- measuring cross-channel generalization: train on speech, test on song and vice versa
- optimizing for cpu inference (target: < 100ms per clip, < 5mb model size)

explicitly out of scope: real-time streaming inference, multilingual ser, continuous arousal-valence prediction.

## goals

1. demonstrate that a 1d cnn on log-mel spectrograms outperforms the mfcc + svm baseline by at least 10 percentage points on speaker-disjoint test splits across multiple scenarios.
2. achieve >= 70% test accuracy on speech 8-class and >= 65% on song 6-class.
3. evaluate cross-channel generalization between speech and song.
4. produce a deployable model that runs on a single cpu core within latency and size budgets.
5. document reproducible training and evaluation pipelines from raw wavs to final results.
