# project goal and success criteria

build a lightweight cnn-based speech emotion recognition system on open datasets and demonstrate that it outperforms classical baselines while remaining deployable on cpu.

## measurable outcomes

| metric | target |
|--------|--------|
| test accuracy (ravdess, 8-class) | >= 70% |
| test accuracy (ravdess, 4-class subset) | >= 80% |
| inference latency on cpu (single clip) | < 100ms |
| model size | < 5mb |
| improvement over mfcc + svm baseline | >= 10 percentage points |

## success criteria

1. cnn model achieves target accuracy on held-out speaker split (cross-speaker evaluation).
2. baseline (mfcc + svm) implemented and evaluated for direct comparison.
3. model runs full inference on a single cpu core within latency budget.
4. training pipeline is reproducible from data download to final evaluation.
5. results documented with confusion matrices, class-wise f1, and cross-speaker analysis.
