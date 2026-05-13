# end-to-end workflow and handoff points

## pipeline phases

| phase | notebook | input | output | handoff |
|-------|----------|-------|--------|---------|
| 1. data acquisition | `01-data-acquisition/` | ravdess urls | `data/raw/` wav files + split dirs | raw files on disk, split into train/val/test |
| 2. eda | `02-eda/` | `data/{train,val,test}/{speech,song}/` | distribution plots, label counts | understanding of class balance, clip lengths, speech vs song |
| 3. preprocessing | `03-data-preprocessing/` | wavs from split dirs | cleaned audio arrays | trimmed, normalized, padded audio |
| 4. feature engineering | `04-feature-engineering/` | cleaned audio | `data/processed/` feature .npy + labels .npy | mel spectrograms (cnn) + mfcc vectors (svm) |
| 5. model training | `05-model-training/` | feature arrays | `data/models/` checkpoints | trained cnn + svm models (3 scenarios each) |
| 6. model evaluation | `06-model-evaluation/` | models + test set | metrics, confusion matrices | performance comparison tables |
| 7. model testing | `07-model-testing/` | held-out test | final results, error analysis | deliverable-ready outputs |

## execution order

notebooks must run in numbered sequence. each phase depends on the output of the previous one. skipping a phase will cause missing file errors in downstream notebooks.

## verification at each handoff

1. **acquisition -> eda**: verify file count (1440 speech + 1012 song = 2452) and split integrity (no actor leaks).
2. **eda -> preprocessing**: confirm all clips load without errors, clip duration distribution is understood.
3. **preprocessing -> features**: confirm output shapes: mel (n_clips, time_frames, 128), mfcc (n_clips, 240).
4. **features -> training**: confirm splits are speaker-disjoint and class labels are balanced.
5. **training -> evaluation**: model checkpoint loads and produces predictions without errors. train/val loss curves converge.
6. **evaluation -> testing**: metrics are reasonable (above chance: >12.5% for 8-class, >16.7% for 6-class).

## training scenarios (run after features are ready)

| scenario | channel | classes | train files | test files | comparison |
|----------|---------|---------|-------------|------------|------------|
| speech 8-class | speech only | 8 | 1140 | 120 | cnn vs svm |
| song 6-class | song only | 6 | 792 | 88 | cnn vs svm |
| combined 8-class | both | 8 | 1932 | 208 | cnn vs svm |
| cross-channel | cross | 8/6 | varies | varies | speech<->song |

## notebook pipeline dependencies

```
01-data-acquisition (already done: data downloaded + split)
       |
       v
02-eda  (reads from data/train/, data/val/, data/test/)
       |
       v
03-data-preprocessing  (reads from split dirs, outputs cleaned arrays)
       |
       v
04-feature-engineering  (reads cleaned arrays, saves .npy)
       |
       v
05-model-training  (reads .npy, trains, saves .pt)
       |
       v
06-model-evaluation  (reads .pt + .npy, produces metrics)
       |
       v
07-model-testing  (final comparison, report figures)
```
