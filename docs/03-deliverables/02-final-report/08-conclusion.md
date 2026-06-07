## 7. conclusion

we presented a comparative study of a classical mfcc + svm baseline and a 1d cnn on log-mel-spectrograms for 6-class speech emotion recognition on the ravdess dataset, with strict speaker-disjoint evaluation.

**key takeaways.**
1. the svm baseline (rbf, c=1) achieves **70.45% test accuracy** and **0.19 ms/sample cpu latency**, outperforming the 1d cnn (66.48% test, 0.53 ms/sample) on this dataset.
2. capping the svm c parameter at {0.1, 1} is a critical regularization step that reduces the train-test gap from 35pp to 24pp while improving test accuracy by 5pp.
3. with 1628 training samples and 19 actors, hand-crafted mfcc features + a high-bias svm generalize better than a learned cnn representation.
4. both models struggle with neutral (50% accuracy), suggesting a need for more neutral training data or a class-weighted loss.

**impact.** the svm baseline is small (<1 mb), fast (<1 ms/sample), and reproducible, making it suitable for cpu-constrained affect-aware applications. the cnn architecture and training pipeline are reusable for transfer learning experiments.

**next steps.** fine-tuning wav2vec 2.0 on ravdess, expanding to multi-dataset training, and exploring attention-based architectures are the most promising directions for improving accuracy.
