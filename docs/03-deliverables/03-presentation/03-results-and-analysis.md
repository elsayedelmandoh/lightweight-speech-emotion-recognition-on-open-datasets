# 03 - results & analysis

## slide 13: quantitative comparison
**table 1: train/val/test accuracy**

| model | train | val | test | train-test gap | params |
|-------|-------|-----|------|----------------|--------|
| svm rbf | 94.47% | 62.88% | **70.45%** | 24.02pp | n/a |
| 1d cnn | 94.90% | **75.38%** | 66.48% | 28.42pp | 132,806 |

- svm wins test (+3.97pp); cnn wins val (+12.5pp)
- cnn overfits more (larger train-test gap)
- small dataset (1628 samples) favors high-bias svm

## slide 14: per-class breakdown
**table 2: per-emotion test accuracy**

| emotion | support | svm rbf | 1d cnn |
|---------|---------|---------|--------|
| neutral | 16 | 50.0% | 50.0% |
| calm | 32 | **81.2%** | 65.6% |
| happy | 32 | 62.5% | 46.9% |
| sad | 32 | 62.5% | **75.0%** |
| angry | 32 | 65.6% | **84.4%** |
| fearful | 32 | **90.6%** | 68.8% |

- svm: excels on fearful (90.6%) and calm (81.2%)
- cnn: excels on angry (84.4%) and sad (75.0%)
- both: struggle with neutral (50%) -- small sample, acoustic similarity to calm

## slide 15: confusion matrices
<img src="../../02-results/figures/fig07-svm_confusion_matrix.png" width="450">
*fig 1. svm test confusion matrix — happy->fearful most common (10/32), both high-arousal*

<img src="../../02-results/figures/fig07-cnn1d_confusion_matrix.png" width="450">
*fig 2. cnn test confusion matrix — happy->calm, fearful->sad, confuses arousal levels*

## slide 16: training curves
<img src="../../02-results/figures/fig05-cnn1d_training_curves.png" width="600">
*fig 3. cnn training curves — train ~95%, val plateaus ~75%, early stopping at epoch 67*

## slide 17: efficiency
**table 3: cpu inference latency**

| model | mean | p50 | p99 | throughput |
|-------|------|-----|-----|------------|
| svm rbf | 0.195 ms | 0.180 ms | 0.331 ms | ~5400/s |
| 1d cnn | 0.530 ms | 0.500 ms | 0.863 ms | ~1900/s |

- svm 2.7x faster
- both under 1 ms target
- cnn overhead: conv1d ops; svm overhead: kernel eval on 1628 support vectors

## slide 18: why svm wins
1. **bias-variance tradeoff:** 1628 samples favors high-bias svm
2. **feature representation:** mfcc+delta is strong hand-crafted feature for emotion
3. **kernel capacity:** rbf + c=1 is moderate capacity -- capping c was key regularization fix
4. literature range: 55-80% for cross-speaker ravdess -- our 70.45% svm is competitive

## slide 19: validation confusion matrices
<img src="../../02-results/figures/fig06-svm_confusion_matrix.png" width="450">
*fig 4. svm validation confusion matrix — same patterns as test*

<img src="../../02-results/figures/fig06-cnn1d_confusion_matrix.png" width="450">
*fig 5. cnn validation confusion matrix — broader confusion across arousal levels*
