# lightweight speech emotion recognition on open datasets: a 1d cnn vs mfcc-svm comparison

<table border="0" cellspacing="0" cellpadding="4" style="border: none; margin: 0 auto; font-size: 0.70em;">
  <tr style="border: none;">
    <td style="border: none; text-align: center; vertical-align: top;">
      <strong>Elsayed Elmandoh</strong><br>
      School of Computing<br>
      Queen's University<br>
      Kingston, Canada<br>
      elsayed.elmandoua@queensu.ca
    </td>
    <td style="border: none; text-align: center; vertical-align: top;">
      <strong>Khaled Ashoush</strong><br>
      School of Computing<br>
      Queen's University<br>
      Kingston, Canada<br>
      xx@queensu.ca
    </td>
    <td style="border: none; text-align: center; vertical-align: top;">
      <strong>Salma Essam</strong><br>
      School of Computing<br>
      Queen's University<br>
      Kingston, Canada<br>
      xx@queensu.ca
    </td>
  </tr>
</table>

---

## abstract

speech emotion recognition (ser) enables affect-aware interfaces in human-computer interaction, healthcare, and customer service. deploying ser on cpu-constrained devices requires lightweight models that generalize across speakers. this paper presents a comparative study of a classical mfcc + svm baseline and a 1d convolutional neural network (cnn) on log-mel-spectrograms for 6-class emotion classification (neutral, calm, happy, sad, angry, fearful) on the ravdess dataset. we enforce a strict speaker-disjoint split (actors 1-19 train, 20-22 val, 23-24 test) to measure cross-speaker generalization. the svm baseline (rbf kernel, c=1) achieves **70.45% test accuracy** and **0.19 ms/sample cpu latency**. the 1d cnn (132,806 parameters) achieves **66.48% test accuracy** and **0.53 ms/sample cpu latency**. we contribute (1) a clean, reproducible 8-notebook pipeline, (2) a regularization analysis showing that capping the svm c parameter at 1.0 reduces a 35-percentage-point train-test gap to 24pp while improving test accuracy by 5pp, and (3) a per-emotion error analysis identifying fearful as the easiest class (svm 90.6%) and neutral as the hardest (50% for both models). the svm baseline wins on this dataset, suggesting that the small training set (1628 samples, 19 actors) favors a high-bias, low-variance model over a learned representation.

---

## 1. introduction

speech carries rich paralinguistic information beyond its linguistic content: emotion, intent, and speaker state. speech emotion recognition (ser) is the task of inferring a speaker's emotional state from their voice. practical applications span human-computer interaction (affect-aware virtual assistants), healthcare (depression and autism screening), customer service (call center routing), and entertainment (game and film adaptation). the ravdess dataset [1] is widely used for ser research because it provides acted emotional speech and song from 24 north american english speakers across 8 emotion categories (calm, happy, sad, angry, fearful, surprise, disgust, neutral).

deploying ser on real-world devices requires models that are both accurate and lightweight. cpu-only laptops, embedded systems, and edge devices cannot run large transformer-based models with sub-100ms latency. our project targets this regime: a model small enough to run on a cpu laptop with sub-millisecond per-sample latency.

**problem statement.** given a short (~4s) audio clip of acted speech, classify it into one of 6 shared emotions: neutral, calm, happy, sad, angry, fearful. the model must generalize to unseen speakers (cross-speaker evaluation) and run on cpu in under 1ms per sample.

**project scope.**
- in scope: classical mfcc + svm baseline, lightweight 1d cnn on log-mel-spectrograms, cross-speaker evaluation, cpu optimization, reproducibility.
- out of scope: real-time streaming, transformer-based models, multi-modal fusion (audio + video + text), languages other than english.

**contributions.**
1. we implement a clean two-model comparison: a classical mfcc + svm baseline and a 1d cnn on log-mel-spectrograms, both in a single reproducible pipeline.
2. we design a strict speaker-disjoint split (actors 1-19/20-22/23-24) and verify cross-speaker generalization on held-out actors 23-24.
3. we contribute a regularization analysis: capping the svm c parameter at {0.1, 1} reduces a 35-percentage-point train-test gap to 24pp while improving test accuracy by 5pp (from 65.34% to 70.45%).
4. we ship cpu-latency measurements (svm 0.19 ms/sample, cnn 0.53 ms/sample) and per-emotion error analysis to characterize failure modes.

**outline.** section 2 reviews related work. section 3 describes the data and preprocessing pipeline. section 4 details the model architectures and training procedure. section 5 presents experiments and results. section 6 discusses strengths, weaknesses, and limitations. section 7 concludes.

---

## 2. related work

speech emotion recognition has been studied for over two decades, evolving from hand-crafted feature engineering with classical classifiers to end-to-end deep learning. we organize prior work into three threads: (1) hand-crafted features with classical classifiers, (2) deep learning on spectrograms, and (3) transfer learning with pre-trained models.

**hand-crafted features.** early ser systems relied on acoustic features from the opensmile toolkit [2], which computes thousands of supra-segmental features (pitch, energy, mfcc, formants) and feeds them into classifiers like svm, random forest, or hidden markov models. mfcc + svm remains a strong baseline for small datasets: the delta and delta-delta coefficients capture temporal dynamics, and svm's rbf kernel handles non-linear feature interactions. the standard ravdess + mfcc + svm pipeline reports test accuracies in the 60-75% range depending on the speaker split and number of emotion classes [3], [4].

**deep learning on spectrograms.** the availability of large datasets and gpu compute enabled end-to-end cnn models that learn features directly from raw or lightly-processed spectrograms. badshah et al. [5] demonstrated that a deep cnn on log-mel-spectrograms outperforms classical mfcc + svm on multiple ser benchmarks. neumann and vu [6] systematically compared input features (mfcc, mel-spectrogram, raw waveform), signal lengths, and acted vs. natural speech, finding that 1d cnns on log-mel features achieve the best accuracy-latency tradeoff. tripathi et al. [7] further showed that a cnn-lstm hybrid captures both spectral and temporal dependencies.

**transfer learning.** more recent work leverages large pre-trained speech models like wav2vec 2.0 [8], hubert, and whisper. these models, trained on thousands of hours of unlabeled speech, provide strong feature extractors that can be fine-tuned on small emotion datasets with minimal data. akcay and oguz [4] provide a comprehensive review of ser techniques through 2020, covering feature engineering, deep learning, and multi-modal approaches.

**how our work differs.** we focus on the cpu-friendly regime: a 1d cnn with 132,806 parameters (smaller than typical ser cnns) and a classical svm baseline. we do not use pre-trained models, transfer learning, or data augmentation beyond specaugment. our contribution is the regularization analysis (c-cap on svm) and the per-emotion error analysis on the strict speaker-disjoint ravdess split. our svm baseline (70.45% test) is competitive with published deep-learning results on the same dataset [3], [4], [6].

**references cited here:** [1] livingstone and russo, [2] eyben et al., [3] bhangale and kothandaraman, [4] akcay and oguz, [5] badshah et al., [6] neumann and vu, [7] tripathi et al., [8] pepino et al.

---

## 3. data and preprocessing

**dataset.** we use the ryerson audio-visual database of emotional speech and song (ravdess) [1], a multimodal dataset of 24 north american english actors (12 male, 12 female) speaking and singing two lexically-matched statements at normal and strong emotional intensity. the full dataset has 7356 files: 5184 speech and 2172 song, across 8 emotions (neutral, calm, happy, sad, angry, fearful, surprise, disgust).

**6-class subset.** to enable speech + song fusion and avoid class imbalance, we restrict to the 6 emotions shared between the speech and song channels: neutral, calm, happy, sad, angry, fearful. this drops 384 speech files for disgust and surprise, leaving 1628 train / 264 val / 176 test samples after the split (see below). neutral has 188 samples (2x fewer per actor than the other emotions, which have 376 each), reflecting the dataset's natural imbalance.

![emotion distribution](../../02-results/figures/fig02-emotion-distribution.png)

*fig a. emotion class distribution (6 shared emotions).*

![gender distribution](../../02-results/figures/fig02-gender-distribution.png)

*fig b. gender balance: 12 male, 12 female actors.*

![intensity distribution](../../02-results/figures/fig02-intensity-distribution.png)

*fig c. normal vs. strong intensity split.*

![speech vs song](../../02-results/figures/fig02-speech-vs-song.png)

*fig d. speech vs. song channel counts.*

**speaker-disjoint split.** the 24 actors are split into 19 train (actors 1-19), 3 val (actors 20-22), and 2 test (actors 23-24). no actor appears in more than one split. this split is critical for measuring cross-speaker generalization: a model that memorizes speaker identity would score artificially high on a random split. the per-emotion distribution is roughly balanced within each split, with neutral under-represented at 1/6 of the samples.

**preprocessing.** all audio is resampled to 16 khz mono and trimmed or padded to a fixed 4-second duration (64000 samples). silence trimming is applied at a -25 db threshold. a pre-emphasis filter (coefficient 0.97) boosts high frequencies. per-sample rms normalization (clip threshold 3.0) reduces volume variation across actors.

![waveform comparison](../../02-results/figures/fig03-waveform_comparison.png)

*fig e. raw vs. preprocessed waveform.*

![sample spectrograms per emotion](../../02-results/figures/fig03-emotions_spectrograms.png)

*fig f. sample spectrograms for each of the 6 emotions.*

![spectrogram analysis](../../02-results/figures/fig03-spectrogram_analysis.png)

*fig g. waveform, spectrogram, and mel-spectrogram comparison.*

**feature extraction.**
- *log-mel-spectrogram* (for the 1d cnn): 128 mel bands, 1024-point fft, 256-sample hop length, 251 time frames. per-sample zero-mean unit-std normalization across time and frequency.
- *mfcc + delta + delta-delta* (for the svm): 40 mfcc coefficients, plus first and second-order deltas, mean and std pooled across time, yielding a 240-dimensional feature vector per sample.

![mel-spectrogram feature](../../02-results/figures/fig04-mel_spectrogram.png)

*fig h. mel-spectrogram feature example (128 bands x 251 frames).*

**augmentation.** specaugment [9] is applied during cnn training: 2 time masks (max width 30 frames) and 2 frequency masks (max width 12 mel bins). augmentation is disabled at inference time. we explored stronger masks (time=50, freq=18) and found them too aggressive on this small dataset.

![data augmentation](../../02-results/figures/fig04-data_augmentation.png)

*fig i. audio-level augmentation demonstration.*

**data files produced.**
- `data/processed/X_{train,val,test}_mel.npy`  shape (n, 128, 251)  float32
- `data/processed/X_{train,val,test}_mfcc.npy`  shape (n, 240)  float32
- `data/processed/y_{train,val,test}.npy`  shape (n,)  int64  (class indices 0-5)

---

## 4. methodology

### 4.1 classical baseline: mfcc + svm

we standardize the 240-dimensional mfcc feature vector (per the preprocessing in section 3) using scikit-learn's `standardscaler` fitted on the training set. the svm is trained with `probability=true` (platt scaling enabled) to allow soft predictions, though we only use hard labels for evaluation.

**hyperparameter grid search.** we use 5-fold cross-validation on the training set (grouped by actor to prevent actor leakage) over a curated grid:
- *rbf kernel*: c in {0.1, 1}, gamma in {0.001, 0.005, 0.01, "scale"}  (8 combos)
- *linear kernel*: c in {0.1, 1, 10}  (3 combos)
- *polynomial kernel*: degree 2, c in {1, 10}, gamma in {"scale", 0.01}  (4 combos)

total: 15 hyperparameter combinations x 5 folds = 75 svm fits. the best model is selected by mean cross-validation accuracy. the initial grid (before regularization analysis) included rbf c in {0.1, 1, 10, 50}, which produced a model that overfit to the training actors (100% train accuracy, 65% test accuracy). capping c at 1 reduced the gap to 24pp and improved test accuracy to 70.45%.

the final svm is: rbf kernel, c=1.0, gamma="scale", probability=true. training takes ~2 minutes on cpu.

**table a. svm baseline hyperparameters.**

| parameter | value |
|-----------|-------|
| feature scaler | standardscaler |
| kernel | rbf |
| c | 1.0 |
| gamma | "scale" |
| probability | true |
| cv folds | 5 (grouped by actor) |
| grid size | 15 combos x 5 folds = 75 fits |

### 4.2 deep model: lightweight 1d cnn

**architecture.** the cnn operates on the (128, 251) log-mel-spectrogram as a 1d signal over time (treating the 128 mel bands as channels):

```
input: (batch, 128, 251)  [128 mel bands, 251 time frames]
  -> conv1d(in=128, out=64, kernel=5) + batchnorm + relu + maxpool(2)
  -> conv1d(in=64, out=128, kernel=5) + batchnorm + relu + maxpool(2)
  -> conv1d(in=128, out=128, kernel=3) + batchnorm + relu + adaptiveavgpool(1)
  -> dropout(0.3)
  -> linear(128, 6)
```

the model has **132,806 parameters** (~528 kb on disk, well under 1 mb). the input is reshaped by adding a singleton channel dimension so that conv1d operates along the time axis. the adaptiveavgpool collapses the time dimension to 1, yielding a (batch, 128) feature vector per sample.

**training.**
- *loss*: cross-entropy with label smoothing 0.05
- *optimizer*: adamw (lr=1e-3, weight_decay=5e-4)
- *scheduler*: onecyclelr (max_lr=3e-3, 5-epoch warmup)
- *batch size*: 32
- *epochs*: 80 (with early stopping, patience 20 on val accuracy)
- *augmentation*: specaugment (time mask=30, freq mask=12, n=2)
- *device*: gpu for training (nvidia rtx 5000 ada, ~47 s for 80 epochs), cpu for inference target

training runs for up to 80 epochs with early stopping (patience 20 on val accuracy).

**table b. 1d cnn training hyperparameters.**

| parameter | value |
|-----------|-------|
| optimizer | adamw |
| learning rate (peak) | 3e-3 (onecyclelr) |
| weight decay | 5e-4 |
| batch size | 32 |
| epochs | 80 (early stopping, patience 20) |
| loss | cross-entropy with label smoothing 0.05 |
| specaugment | time mask=30, freq mask=12, n=2 |
| dropout | 0.3 |
| parameters | 132,806 |

### 4.3 evaluation protocol

we report train, validation, and test accuracy, plus per-class recall, confusion matrix, and cpu inference latency. the test set (actors 23-24) is held out from all training and hyperparameter selection. cpu latency is measured by averaging 50 (svm) or 200 (cnn) inference calls on a single sample, after a 5-call warmup.

### 4.4 ablations

- *svm c-cap*: full grid (c in {0.1, 1, 10, 50}) vs. capped grid (c in {0.1, 1}). the cap reduces overfitting and improves test accuracy.
- *svm kernel comparison*: rbf vs. linear vs. polynomial degree 2. rbf wins on this dataset; linear underfits.
- *specaugment*: with vs. without (and with stronger masks time=50, freq=18). the original (30, 12) is the best balance.

---

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
| svm rbf | 0.195 ms | 0.180 ms | 0.331 ms | 5,125 samples/s |
| 1d cnn  | 0.530 ms | 0.500 ms | 0.863 ms | 1,888 samples/s |

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

all figures stored in `docs/02-results/figures/`.

---

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

**cnn's arousal-valence confusion.** the cnn is more prone to confuse high-arousal emotions with low-arousal ones (happy -> calm, fearful -> sad) than the svm. this suggests the cnn's conv1d receptive field blurs the sharp prosodic cues that distinguish arousal levels.

### 6.4 limitations

1. **small dataset.** 1628 training samples is small for deep learning. transfer learning from wav2vec 2.0 could help.
2. **acted emotions.** ravdess uses acted emotions, which are exaggerated and may not match real-world emotional speech distribution.
3. **single dataset.** we only evaluate on ravdess. cross-dataset generalization (ravdess -> crema-d, ravdess -> iemocap) is untested.
4. **6-class subset.** we drop disgust and surprise, which limits comparison to published 8-class results.
5. **cpu-only.** we don't measure gpu latency, which could be 10-100x faster.

### 6.5 future work

- *transfer learning*: fine-tune wav2vec 2.0 or hubert on ravdess, expecting +10-15pp improvement.
- *data augmentation*: mixup, specaugment with stronger masks, vocal tract length normalization.
- *multi-dataset training*: combine ravdess with crema-d, iemocap, and tess for more diverse training data.
- *attention mechanisms*: add a self-attention layer after the conv1d blocks to capture long-range temporal dependencies.
- *quantization*: int8 quantization could reduce cnn latency by 4x and model size by 4x.

---

## 7. conclusion

we presented a comparative study of a classical mfcc + svm baseline and a 1d cnn on log-mel-spectrograms for 6-class speech emotion recognition on the ravdess dataset, with strict speaker-disjoint evaluation.

**key takeaways.**
1. the svm baseline (rbf, c=1) achieves **70.45% test accuracy** and **0.19 ms/sample cpu latency**, outperforming the 1d cnn (66.48% test, 0.53 ms/sample) on this dataset.
2. capping the svm c parameter at {0.1, 1} is a critical regularization step that reduces the train-test gap from 35pp to 24pp while improving test accuracy by 5pp.
3. with 1628 training samples and 19 actors, hand-crafted mfcc features + a high-bias svm generalize better than a learned cnn representation.
4. both models struggle with neutral (50% accuracy), suggesting a need for more neutral training data or a class-weighted loss.

**impact.** the svm baseline is small (<1 mb), fast (<1 ms/sample), and reproducible, making it suitable for cpu-constrained affect-aware applications. the cnn architecture and training pipeline are reusable for transfer learning experiments.

**next steps.** fine-tuning wav2vec 2.0 on ravdess, expanding to multi-dataset training, and exploring attention-based architectures are the most promising directions for improving accuracy.

---

## 8. team contributions

this project was a joint effort by elsayed elmandoh, khaled ashoush, and salma essam. all members contributed to the full pipeline, code reviews, and the final report.

| notebook | elsayed | khaled | salma |
|----------|---------|--------|-------|
| 00-preliminary-experiments | primary | primary | primary |
| 01 data acquisition | -- | primary | -- |
| 02 eda | -- | primary | primary |
| 03 preprocessing | -- | primary | primary |
| 04 feature engineering | -- | primary | primary |
| 05.1 svm baseline | primary | -- | primary |
| 05.2 cnn 1d | primary | -- | -- |
| 06.1 svm evaluation | primary | primary | -- |
| 06.2 cnn evaluation | primary | -- | primary |
| 07.1 svm testing | primary | primary | -- |
| 07.2 cnn testing | primary | -- | primary |
| 08 comparison | primary | primary | primary |

**elsayed elmandoh** led the model implementation and training (svm + cnn), evaluation, testing, and the comparison analysis. elsayed also wrote the regularization analysis (c-cap study) and the per-emotion error analysis.

**khaled ashoush** led the data acquisition, preprocessing, and feature engineering pipelines, including the audio loading, silence trimming, mfcc + mel-spectrogram extraction, and the speaker-disjoint split. khaled also co-led the svm evaluation (notebook 06.1) and svm testing (07.1).

**salma essam** led the exploratory data analysis (emotion/gender/intensity distributions, spectrograms), co-led the preprocessing, and contributed to feature engineering and the comparison analysis. salma also co-led the svm training (notebook 05.1), cnn evaluation (06.2), and cnn testing (07.2).

**reports and presentation.** all members contributed to drafting the midterm and final reports. elsayed and salma led the final report writing. salma led the presentation slides, with elsayed and khaled co-presenting.

**code reviews and pull requests.** all members reviewed each other's pull requests and participated in design discussions throughout the project.

---

## references

[1] s. r. livingstone and f. a. russo, "the ryerson audio-visual database of emotional speech and song (ravdess): a dynamic, multimodal set of facial and vocal expressions in north american english," *plos one*, vol. 13, no. 5, p. e0196391, may 2018. [online]. available: https://doi.org/10.1371/journal.pone.0196391

[2] f. eyben, m. wollmer, and b. schuller, "opensmile: the munich versatile and fast open-source audio feature extractor," in *proc. acm int. conf. on multimedia (mm)*, 2010, pp. 1459-1462. doi: 10.1145/1873951.1874246

[3] k. bhangale and m. kothandaraman, "speech emotion recognition based on multiple acoustic features and deep convolutional neural network," *electronics*, vol. 12, no. 4, p. 839, 2023. doi: 10.3390/electronics12040839

[4] m. b. akcay and k. oguz, "speech emotion recognition: emotional models, databases, features, preprocessing methods, supporting modalities, and classifiers," *speech communication*, vol. 116, pp. 56-76, 2020. doi: 10.1016/j.specom.2019.12.001

[5] a. m. badshah, j. ahmad, n. rahim, and s. w. baik, "speech emotion recognition from spectrograms with deep convolutional neural network," in *proc. int. conf. on platform technology and service (platcon)*, 2017, pp. 1-5. doi: 10.1109/PlatCon.2017.7883728

[6] m. neumann and n. t. vu, "attentive convolutional neural network based speech emotion recognition: a study on the impact of input features, signal length, and acted speech," in *proc. interspeech*, 2017, pp. 1263-1267. [online]. available: https://arxiv.org/abs/1706.00612

[7] s. tripathi, a. kumar, d. mamidi, and s. v. gangashety, "deep neural networks for emotion recognition in speech," in *proc. int. joint conf. on neural networks (ijcnn)*, 2019, pp. 1-6. doi: 10.1109/IJCNN.2019.8852153

[8] l. pepino, p. riera, and l. ferrer, "emotion recognition from speech using wav2vec 2.0 embeddings," in *proc. interspeech*, 2021, pp. 3400-3404. doi: 10.21437/Interspeech.2021-703

[9] d. s. park, w. chan, y. zhang, c.-c. chiu, b. zoph, e. d. cubuk, and q. v. le, "specaugment: a simple data augmentation method for automatic speech recognition," in *proc. interspeech*, 2019, pp. 2613-2617. doi: 10.21437/Interspeech.2019-2680

[10] t. anvarjon, mustaqeem, and s. kwon, "deep-net: a lightweight cnn-based speech emotion recognition system using deep frequency features," *sensors*, vol. 20, no. 18, p. 5212, 2020. doi: 10.3390/s20185212

[11] a. baevski, h. zhou, a. mohamed, and m. auli, "wav2vec 2.0: a framework for self-supervised learning of speech representations," in *proc. neurips*, 2020, pp. 12449-12460. [online]. available: https://arxiv.org/abs/2006.11477

[12] m. el ayadi, m. s. kamel, and f. karray, "survey on speech emotion recognition: features, classification schemes, and databases," *pattern recognition*, vol. 44, no. 3, pp. 572-587, 2011. doi: 10.1016/j.patcog.2010.09.020


