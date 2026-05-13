# project goal and success criteria

build a lightweight cnn-based speech emotion recognition system on open datasets and demonstrate that it outperforms classical baselines while remaining deployable on cpu.

## measurable outcomes

### speech 8-class (core experiment)

| metric | target |
|--------|--------|
| test accuracy | >= 70% |
| macro f1 | >= 0.65 |
| inference latency on cpu | < 100ms per clip |
| model size | < 5mb |
| improvement over mfcc + svm baseline | >= 10 percentage points |

### song 6-class (secondary)

| metric | target |
|--------|--------|
| test accuracy | >= 65% |
| macro f1 | >= 0.60 |

### combined speech+song 8-class (best model)

| metric | target |
|--------|--------|
| test accuracy | >= 72% |

### cross-channel generalization

| scenario | target |
|----------|--------|
| train speech, test song | report accuracy |
| train song, test speech | report accuracy |

## success criteria

1. cnn model achieves target accuracy on held-out speaker split (cross-speaker evaluation).
2. all three training scenarios (speech-only, song-only, combined) implemented and compared.
3. baseline (mfcc + svm) implemented on same splits for direct comparison.
4. model runs full inference on a single cpu core within latency budget.
5. training pipeline is reproducible from raw wavs to final evaluation.
6. cross-channel generalization (speech<->song) measured and reported.
7. results documented with confusion matrices, class-wise f1, per-speaker breakdown, and cross-speaker analysis.
