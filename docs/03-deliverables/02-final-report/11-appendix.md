## appendix

### a. hyperparameter tables

**table a1. svm baseline hyperparameters (final, post c-cap).**

| parameter | value |
|-----------|-------|
| feature scaler | standardscaler |
| kernel | rbf |
| c | 1.0 |
| gamma | "scale" |
| probability | true |
| cv folds | 5 (grouped by actor) |
| grid size | 15 combos x 5 folds = 75 fits |

**table a2. 1d cnn training hyperparameters.**

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
