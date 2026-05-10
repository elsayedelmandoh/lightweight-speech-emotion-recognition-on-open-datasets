# related work and prior art

## key papers

### neumann & vu (2017) - attentive cnn for ser
- paper: "attentive convolutional neural network based speech emotion recognition: a study on the impact of input features, signal length, and acted speech"
- venue: interspeech 2017
- link: https://arxiv.org/abs/1706.00612
- contribution: studies how input feature type (mel, mfcc, spectrogram), signal length, and acted vs natural speech affect cnn-based ser. introduces attention mechanism over time frames. shows mel spectrograms outperform mfccs for cnn input.

### tripathi et al. (2019) - deep neural networks for emotion recognition
- paper: "deep neural networks for emotion recognition in speech"
- venue: ijcnn 2019
- link: https://doi.org/10.1109/IJCNN.2019.8852153
- contribution: evaluates multiple deep architectures (cnn, lstm, cnn-lstm) on iemocap and emodb. reports that combining spectral and temporal features improves accuracy.

## reference implementations

- tuncayka/speech_emotion - [github](https://github.com/tuncayka/speech_emotion)
- marcogdepinto/emotion-recognition-english - [github](https://github.com/marcogdepinto/emotion-recognition-english)

## classical baselines

- mfcc + svm is the standard lightweight baseline for ser. typically achieves 50-65% accuracy on ravdess depending on emotion subset and train/test split strategy.
- newer work uses log-mel spectrograms as cnn input, which captures more frequency detail than mfccs alone.

## gaps this project addresses

- most reference implementations use 2d cnns on mel images or are not optimized for inference speed.
- no published comparison of a 1d cnn on raw mel spectrograms vs mfcc + svm specifically targeting cpu deployment on ravdess.
