# related work

## key papers

### paper 1: livingstone & russo (2018) - the ravdess dataset

livingstone and russo [1] introduced the ryerson audio-visual database of emotional speech and song (ravdess), a dataset of 7356 files across 24 professional actors expressing emotions through speech and song. the dataset was validated by 247 human raters on emotional validity, intensity, and genuineness, with high interrater reliability reported. the audio-only subset (2452 files) serves as the primary benchmark for our work. the dataset's controlled recording conditions and comprehensive emotion labelling make it a standard reference for ser research, though its use of acted rather than naturalistic speech may overestimate real-world model performance.

### paper 2: neumann & vu (2017) - attentive cnn for ser

neumann and vu [2] proposed an attentive convolutional neural network for speech emotion recognition and systematically studied the impact of input features, signal length, and acted speech on performance. their key findings include: mel spectrograms outperform mfccs as cnn input features; attention over time frames improves classification by weighting emotionally salient regions; and acted speech yields higher accuracy than naturalistic speech. our project builds on their finding that mel spectrograms are superior cnn inputs, but we explore 1d convolutions instead of their 2d approach, targeting a much smaller model suitable for cpu deployment.

### paper 3: tripathi et al. (2019) - deep neural networks for ser

tripathi et al. [3] evaluated multiple deep architectures including cnns, lstms, and hybrid cnn-lstm models on the iemocap and emodb datasets. they reported that combining spectral and temporal features improves accuracy over either alone, and that cnn-lstm hybrids achieve the best performance but at significantly higher computational cost. they also found that careful data preprocessing substantially impacts results. we adopt their recommendation for preprocessing but choose a simpler 1d cnn architecture to maintain cpu deployability.

### paper 4: mfcc and lstm-based ser

a recent study [4] proposed using mfcc features with lstm networks for speech emotion recognition, achieving strong results on benchmark datasets. the work demonstrates that sequential models can capture temporal dependencies in emotional speech, but lstm-based approaches are computationally heavier than cnn-only alternatives. our 1d cnn seeks to achieve competitive accuracy with lower inference cost, making it more suitable for deployment.
---

## how our project builds on them/differs

