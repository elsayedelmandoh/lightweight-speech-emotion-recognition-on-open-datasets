## 5. experiments and results

### 5.1 quantitative comparison

table 1 summarizes train, validation, and test accuracy for both models on the speaker-disjoint ravdess split.

**table 1. train/val/test accuracy.**

| model   | train  | val    | test   | train-test gap | parameters |
|---------|--------|--------|--------|----------------|------------|
| svm rbf | 94.47% | 62.88% | **70.45%** | 24.02pp        | n/a (kernel method) |
| 1d cnn  | 94.90% | **75.38%** | 66.48% | 28.42pp | 132,806 |

the svm baseline wins on the test set (70.45% vs. 66.48%, +3.97pp), despite having lower validation accuracy. the cnn wins on validation (75.38% vs. 62.88%, +12.5pp), suggesting it overfits the training actors more than the svm. this is consistent with the larger train-test gap for the cnn (28.42pp vs. 24.02pp).

### 5.2 per-class breakdown (test set)

**table 2. per-emotion test accuracy.**

| emotion  | support | svm rbf | 1d cnn |
|----------|---------|---------|--------|
| neutral  | 16      | 50.0%   | 50.0%  |
| calm     | 32      | **81.2%** | 65.6% |
| happy    | 32      | 62.5%   | 46.9%  |
| sad      | 32      | 62.5%   | **75.0%** |
| angry    | 32      | 65.6%   | **84.4%** |
| fearful  | 32      | **90.6%** | 68.8% |

the svm excels on calm (81.2%) and fearful (90.6%); the cnn excels on sad (75.0%) and angry (84.4%). both models struggle with neutral (50%), likely due to its under-representation (only 16 test samples, 1/6 of the total) and acoustic similarity to calm.

### 5.3 efficiency

**table 3. cpu inference latency (per sample).**

| model  | mean    | p50     | p99     | throughput   |
|--------|---------|---------|---------|--------------|
| svm rbf | 0.195 ms | 0.180 ms | 0.331 ms | ~5,400 samples/s |
| 1d cnn  | 0.530 ms | 0.500 ms | 0.863 ms | ~1,900 samples/s |

the svm is ~2.7x faster per sample than the cnn. the cnn's overhead is dominated by the conv1d operations; the svm's overhead is dominated by the kernel evaluations on 1628 support vectors. both meet the project's sub-millisecond latency target.

### 5.4 confusion matrix analysis

![svm test confusion matrix](../../02-results/figures/fig07-svm_confusion_matrix.png)

*fig 1. svm confusion matrix on the test set (actors 23-24).*

![1d cnn test confusion matrix](../../02-results/figures/fig07-cnn1d_confusion_matrix.png)

*fig 2. 1d cnn confusion matrix on the test set (actors 23-24).*

the svm's most common confusion is happy -> fearful (10 misclassifications out of 32 happy samples). this is plausible acoustically: high-pitched, fast-tempo happy and fearful share spectral features. the cnn's most common confusions are happy -> calm (8 misclassifications) and fearful -> sad (5 misclassifications). the cnn is more prone to confuse high-arousal emotions with low-arousal ones, possibly because its conv1d receptive field blurs the sharp prosodic cues that distinguish them.

### 5.5 figures

**training curves.**

![cnn training curves](../../02-results/figures/fig05-cnn1d_training_curves.png)

*fig 3. cnn training/validation accuracy (top) and loss (bottom) over 80 epochs. early stopping triggered at epoch 67 (patience 20).*

**validation confusion matrices.**

![svm validation confusion matrix](../../02-results/figures/fig06-svm_confusion_matrix.png)

*fig 4. svm confusion matrix on the validation set (actors 20-22).*

![cnn validation confusion matrix](../../02-results/figures/fig06-cnn1d_confusion_matrix.png)

*fig 5. 1d cnn confusion matrix on the validation set (actors 20-22).*
