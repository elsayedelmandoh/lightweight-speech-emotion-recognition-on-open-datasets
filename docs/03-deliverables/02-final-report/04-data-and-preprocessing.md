## 3. data and preprocessing

**dataset.** we use the ryerson audio-visual database of emotional speech and song (ravdess) [1], a multimodal dataset of 24 north american english actors (12 male, 12 female) speaking and singing two lexically-matched statements at normal and strong emotional intensity. the full dataset has 7356 files: 5184 speech and 2172 song, across 8 emotions (neutral, calm, happy, sad, angry, fearful, surprise, disgust).

**6-class subset.** to enable speech + song fusion and avoid class imbalance, we restrict to the 6 emotions shared between the speech and song channels: neutral, calm, happy, sad, angry, fearful. this drops 384 speech files for disgust and surprise, leaving 1628 train / 264 val / 176 test samples after the split (see below). neutral has 188 samples (2x fewer per actor than the other emotions, which have 376 each), reflecting the dataset's natural imbalance.

**speaker-disjoint split.** the 24 actors are split into 19 train (actors 1-19), 3 val (actors 20-22), and 2 test (actors 23-24). no actor appears in more than one split. this split is critical for measuring cross-speaker generalization: a model that memorizes speaker identity would score artificially high on a random split. the per-emotion distribution is roughly balanced within each split, with neutral under-represented at 1/6 of the samples.

**preprocessing.** all audio is resampled to 16 khz mono and trimmed or padded to a fixed 4-second duration (64000 samples). silence trimming is applied at a -25 db threshold. a pre-emphasis filter (coefficient 0.97) boosts high frequencies. per-sample rms normalization (clip threshold 3.0) reduces volume variation across actors.

**feature extraction.**
- *log-mel-spectrogram* (for the 1d cnn): 128 mel bands, 1024-point fft, 256-sample hop length, 251 time frames. per-sample zero-mean unit-std normalization across time and frequency.
- *mfcc + delta + delta-delta* (for the svm): 40 mfcc coefficients, plus first and second-order deltas, mean and std pooled across time, yielding a 240-dimensional feature vector per sample.

**augmentation.** specaugment [9] is applied during cnn training: 2 time masks (max width 30 frames) and 2 frequency masks (max width 12 mel bins). augmentation is disabled at inference time. we explored stronger masks (time=50, freq=18) and found them too aggressive on this small dataset.

**data files produced.**
- `data/processed/X_{train,val,test}_mel.npy`  shape (n, 128, 251)  float32
- `data/processed/X_{train,val,test}_mfcc.npy`  shape (n, 240)  float32
- `data/processed/y_{train,val,test}.npy`  shape (n,)  int64  (class indices 0-5)
