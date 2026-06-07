# 04 - limitations & future work

## slide 20: limitations
1. **small dataset:** 1628 training samples is small for deep learning
2. **acted emotions:** ravdess acted emotions are exaggerated vs natural speech
3. **single dataset:** cross-dataset generalization untested (ravdess -> crema-d, iemocap)
4. **6-class subset:** dropped disgust and surprise -- limits comparison to 8-class results
5. **cpu-only:** no gpu latency measurements (would be 10-100x faster)

## slide 21: future work
1. **transfer learning:** fine-tune wav2vec 2.0 or hubert -- expected +10-15pp improvement
2. **data augmentation:** mixup, stronger specaugment, vocal tract length normalization
3. **multi-dataset training:** combine ravdess + crema-d + iemocap + tess
4. **attention:** self-attention after conv1d blocks for long-range dependencies
5. **quantization:** int8 quantization could reduce cnn latency 4x, size 4x

## slide 22: conclusion
- clean, reproducible comparison of svm vs 1d cnn on ravdess
- svm achieves 70.45% test accuracy, 0.19 ms/sample -- wins on this dataset
- capping svm c was key regularization insight (+5pp test accuracy)
- both models meet sub-1ms cpu latency target
- full open-source pipeline: 8 notebooks, typing, configs, docs
- code: [github repo]
