# team contributions

## student a - audio preprocessing and baseline

### completed
- downloaded and verified ravdess dataset (1440 audio files).
- built filename parser to extract emotion, intensity, statement, repetition, actor, and gender labels.
- implemented preprocessing pipeline: silence trimming, amplitude normalization, fixed-length padding.
- ran exploratory data analysis: class distribution, clip durations, waveform and spectrogram visualization.

### planned
- finalize mfcc feature extraction pipeline.
- implement and train svm baseline with grid search.
- implement data augmentation (time shift, noise injection, speed perturbation).

## student b - cnn implementation and training

### completed
- designed 1d cnn architecture (3 conv blocks, global average pooling, fully connected head).
- implemented log-mel spectrogram extraction prototype.
- verified feature shapes and caching pipeline.

### planned
- implement full cnn training loop in pytorch (loss, optimizer, scheduler, early stopping).
- run training experiments with hyperparameter tuning.
- run ablation experiments (number of mel bands, conv blocks, regularization).

## student c - evaluation and report

### completed
- defined evaluation metrics: accuracy, per-class f1, confusion matrix, latency, model size.
- set up speaker-disjoint train/validation/test split (actors 1-18 / 19-21 / 22-24).
- drafted midterm report.

### planned
- run full evaluation on test set for both cnn and svm.
- cross-speaker analysis: per-speaker accuracy, gender breakdown, intensity comparison.
- measure inference latency and model size for deployment report.
- compile final report and presentation.
