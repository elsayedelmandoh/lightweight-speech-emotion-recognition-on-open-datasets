# preliminary experiments and results

## current status

as of the midterm checkpoint, we have completed the full sample-based pipeline: data acquisition, exploratory data analysis, preprocessing, feature engineering, and an initial mfcc + svm baseline run on a representative subset (416 files, 17% of the full dataset). all 7 notebooks in `notebooks/00-preliminary-experiments/` have been executed end-to-end.

## dataset overview (sample subset)

| split | actors | speech | song | total |
|-------|--------|--------|------|-------|
| train | 01, 02 | 120 | 88 | 208 |
| val | 20 | 60 | 44 | 104 |
| test | 23 | 60 | 44 | 104 |
| **total** | 4 | 240 | 176 | **416** |

105 files per actor per channel. actors chosen to cover both genders and all three splits.

## preprocessing metrics

verified on all 416 files:

| step | result |
|------|--------|
| load + trim + normalize | 416 clips, 14.9s total (35.9ms per clip) |
| typical trim reduction | 4.40s -> 2.36s (silence removal) |
| final clip length | 3.00s (144000 samples at 48khz) |
| amplitude normalization | [-1, 1] range verified |

## feature extraction

| feature | shape per clip | total time (240 speech files) |
|---------|---------------|------------------------------|
| log-mel spectrogram | (t, 128) where t varies by duration | ~8s |
| mfcc (40 + delta + delta2, mean+std) | (240,) | ~25s for 208 train files |

## mfcc + svm baseline results

trained on 208 clips (actors 01-02), tested on 104 clips (held-out actor 23).

### overall metrics

| metric | value |
|--------|-------|
| test accuracy | **27.9%** (29/104) |
| macro f1 | 0.238 |
| weighted f1 | 0.260 |
| random chance (8-class) | 12.5% |
| improvement over chance | **2.2x** |
| feature extraction | 25.0s for 208 clips (120ms/clip) |
| svm training | 0.016s |
| inference (single) | 0.425ms |
| inference (batch 32) | 1.796ms (0.056ms per clip) |
| model size | 412 kb |

### per-class analysis

| emotion | f1-score | accuracy | most confused with |
|---------|----------|----------|-------------------|
| neutral | 0.222 | 12% (1/8) | fearful (3/8) |
| calm | 0.400 | 44% (7/16) | surprised (5/16) |
| happy | 0.467 | 44% (7/16) | angry (5/16) |
| sad | 0.000 | 0% (0/16) | surprised (6/16) |
| angry | 0.400 | 44% (7/16) | happy (4/16) |
| fearful | 0.207 | 19% (3/16) | calm (4/16) |
| disgust | 0.000 | 0% (0/8) | surprised (5/8) |
| surprised | 0.205 | 50% (4/8) | angry (4/8) |

### per-channel analysis

| channel | accuracy | count |
|---------|----------|-------|
| speech | 18.3% (11/60) | actor 23 speaking |
| song | 40.9% (18/44) | actor 23 singing |

song performs better than speech. hypothesis: song has more sustained, exaggerated vocal patterns that are easier to distinguish.

### per-intensity analysis

| intensity | accuracy | count |
|-----------|----------|-------|
| normal | 23.2% (13/56) | |
| strong | 33.3% (16/48) | |

strong intensity yields higher accuracy, consistent with expectation that exaggerated emotions are easier to classify.

### confusion patterns

the normalized confusion matrix reveals:
- **sad** (0% accuracy) is almost never predicted correctly, most often confused with surprised and calm
- **disgust** (0%) is also never correctly identified, primarily classified as surprised
- **surprised** has the highest per-class accuracy (50%) but is also the most common false prediction (model defaults to surprised for uncertain cases)
- high-arousal emotions (angry, happy) are mutually confusable, as are low-arousal (calm, sad, neutral)

these patterns are expected when training on only 2 actors. with 19 training actors, the model will learn more robust emotion-specific features and reduce these confusions.

## implementation details

| component | detail |
|-----------|--------|
| language | python 3.12.13 |
| audio loading | librosa 0.11.0 |
| machine learning | scikit-learn 1.8.0 (svm, scaling, metrics) |
| data handling | numpy, pandas |
| visualization | matplotlib, seaborn |
| model persistence | joblib |
| environment | conda on wsl2 (ubuntu) |
| hardware | 4 cpu cores, 8.3gb ram |
| pipeline | git-tracked jupyter notebooks |


