# stack overview and tooling choices

## core stack
- language: python 3.12
- environment: conda
- packages: pip install -r requirements.txt (currently only pytest)
- entrypoint: app.py (currently broken imports - use notebooks instead)
- reusable code: src/
- tests: tests/
- notebooks: notebooks/
- docs: docs/
- data layout: data/{raw,train,val,test,processed,samples,models,predictions}
- ide: vscode (wsl2)

## common libraries

### audio processing
- librosa: loading wav, mel spectrogram, mfcc, silence trimming, augmentation
- numpy: array operations, feature caching (.npy)
- scipy: wav i/o alternative

### deep learning
- pytorch: 1d cnn model, training loop, checkpointing, torchscript export

### machine learning
- scikit-learn: svm, grid search, metrics (accuracy, f1, confusion_matrix), train_test_split

### visualization
- matplotlib: training curves, confusion matrix heatmaps
- seaborn: advanced confusion matrix, per-class metrics plots

### data handling
- pandas: filename parsing, label dataframes, per-speaker analysis


