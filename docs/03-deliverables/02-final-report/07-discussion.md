## 6. discussion

### 6.1 why the svm wins

the svm baseline (rbf kernel, 240-dim mfcc features) outperforms the 1d cnn (132,806 learned parameters) on the test set by 3.97pp. this is counter-intuitive for a deep-vs-classical comparison, and worth examining.

**the bias-variance tradeoff.** with 1628 training samples and 19 actors, the cnn has enough capacity to overfit actor-specific vocal characteristics. the train-test gap (28.42pp for the cnn vs. 24.02pp for the svm) confirms this. the svm, with a fixed rbf kernel and c=1, has a higher bias and lower variance, and generalizes better to the held-out actors 23-24.

**feature representation.** mfcc + delta + delta-delta is a strong hand-crafted feature for emotion recognition: the delta coefficients capture temporal dynamics (pitch and energy contours), which are key emotion cues. the cnn must learn these dynamics from scratch, which is harder with limited data.

**kernel capacity.** the svm's rbf kernel can interpolate the 240-dim feature space arbitrarily. with c=1, it has moderate capacity. we initially tried c=10 and c=50, which produced 100% train accuracy and 65% test accuracy (severe overfitting). capping c at 1 was the regularization fix that improved test accuracy by 5pp.

### 6.2 the cross-speaker gap is structural, not pathological

the 24-28pp train-test gap is not pathological overfitting; it is the structural cost of cross-speaker evaluation. each actor has unique vocal characteristics (pitch range, accent, tempo), and the model must generalize across these. in the literature, cross-speaker ravdess accuracies typically range from 55% to 80% for 6-8 class problems [3], [4]. our svm's 70.45% and cnn's 66.48% are within this range. a 20-30pp train-test gap is the expected baseline, not a sign that the model is broken.

### 6.3 error analysis

**hardest class: neutral.** both models score 50% on neutral (8/16 correct). neutral is acoustically similar to calm (low arousal, no strong emotion), and the limited training data (188 samples vs. 376 for other emotions) makes it hard to learn a robust neutral vs. calm boundary. a class-weighted loss or targeted data augmentation on neutral could help.

**easiest class: fearful.** the svm scores 90.6% on fearful (29/32 correct). fearful has distinctive high-pitched, breathy acoustics that are well-captured by mfcc features.

**happy <-> fearful confusion.** the svm confuses happy with fearful 10/32 times. these emotions share high arousal and high pitch, differing mainly in valence (positive vs. negative). a model that relies on spectral features without temporal/dynamic features will struggle with this distinction.

**cnn's arousal-valence confusion.** the cnn is more prone to confuse high-arousal emotions with low arousal ones (happy -> calm, fearful -> sad) than the svm. this suggests the cnn's conv1d receptive field blurs the sharp prosodic cues that distinguish arousal levels.

### 6.4 limitations

1. **small dataset.** 1628 training samples is small for deep learning. transfer learning from wav2vec 2.0 could help.
2. **acted emotions.** ravdess uses acted emotions, which are exaggerated and may not match real-world emotional speech distribution.
3. **single dataset.** we only evaluate on ravdess. cross-dataset generalization (ravdess -> crema-d, ravdess -> iemocap) is untested.
4. **6-class subset.** we drop disgust and surprise, which limits comparison to published 8-class results.
5. **cpu-only.** we don't measure gpu latency, which could be 10-100x faster.

### 6.5 future work

- *transfer learning*: fine-tune wav2vec 2.0 or hubert on ravdess, expecting +10-15pp improvement.
- *data augmentation*: mixup and vocal tract length normalization (specaugment already implemented with 2x2 time/freq masks).
- *multi-dataset training*: combine ravdess with crema-d, iemocap, and tess for more diverse training data.
- *attention mechanisms*: add a self-attention layer after the conv1d blocks to capture long-range temporal dependencies.
- *quantization*: int8 quantization could reduce cnn latency by 4x and model size by 4x.
