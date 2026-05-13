# planned work and timeline

## remaining experiments

### phase a: feature engineering (notebook 04)

1. **log-mel spectrograms for cnn**
   - input: trimmed wavs from `data/{train,val,test}/{speech,song}/`
   - compute log-mel spectrogram (n_mels=128, n_fft=2048, hop_length=512)
   - output shape per clip: (282, 128) -> save as .npy arrays
   - separate files for speech (1440), song (1012), and combined (2452)

2. **mfcc vectors for svm baseline**
   - extract 40 mfccs + delta + delta-delta per frame
   - aggregate as mean+std per clip -> 240-dim vectors
   - same split structure as mel features

3. **save label arrays**
   - emotion class ints for each clip
   - one-hot optional for cnn training

### phase b: model training (notebook 05)

4. **train svm baseline** (all 3 scenarios)
   - speech-only 8-class: 1140 train files
   - song-only 6-class: 792 train files
   - combined 8-class: 1932 train files
   - grid search c=[0.1,1,10,100], gamma=['scale','auto',0.01,0.001]
   - evaluate on test set: accuracy, per-class f1, confusion matrix

5. **train 1d cnn** (all 3 scenarios)
   - implement 3-block architecture in pytorch
   - cross-entropy loss, adam (lr=1e-3), cosine annealing, batch=32
   - early stopping (patience=15) on validation loss
   - log training curves (loss + accuracy per epoch)

6. **cross-speaker analysis**
   - per-speaker accuracy on test actors 23-24
   - gender breakdown: male vs female accuracy
   - intensity breakdown: normal vs strong accuracy

### phase c: cross-channel and ablation (notebook 06)

7. **cross-channel experiments**
   - train on speech, test on song (8-class -> 6-class subset)
   - train on song, test on speech (6-class -> 8-class partial)
   - report accuracy degradation vs within-channel

8. **ablation experiments**
   - vary n_mels: [64, 128, 256]
   - vary conv blocks: [2, 3, 4]
   - with/without batchnorm, dropout, weight decay

### phase d: deployment and final report (notebook 07)

9. **deployment evaluation**
   - measure cpu inference latency (single clip, batch of 32)
   - measure model size in mb
   - export best model as torchscript

10. **final report and presentation**
    - compile ieee-format final report
    - prepare presentation slides

## risks and mitigation

| risk | likelihood | impact | mitigation |
|------|-----------|--------|------------|
| overfitting on 2452 files | high | high | dropout, weight decay, early stopping; augmentation if needed |
| poor cross-speaker generalization | medium | high | speaker-disjoint splits from the start; report per-speaker results |
| 1d cnn underperforms svm | low | high | fallback to wider 1d cnn (512 channels); add 4th conv block |
| class imbalance (disgust/surprise from speech only) | medium | medium | weighted loss; report per-class f1 not just accuracy |
| song performance much lower than speech | medium | medium | treat as expected result; cross-channel is inherently harder |

## timeline

| phase | tasks | deliverables |
|-------|-------|-------------|
| midterm (complete) | data acquisition, eda, preprocessing pipeline, midterm report | split data, split_labels.csv, midterm report |
| next: phase a | feature extraction (mel + mfcc) | .npy feature arrays for all 2452 clips |
| phase b | svm baseline + cnn training | trained models, training curves, test metrics |
| phase c | cross-channel, ablation | cross-channel accuracy table, ablation results |
| phase d | deployment eval, final report, presentation | model export, final report pdf, slides |
