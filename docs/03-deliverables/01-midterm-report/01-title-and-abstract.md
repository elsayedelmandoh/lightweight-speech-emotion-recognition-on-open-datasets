# title and abstract

## title

lightweight speech emotion recognition on open datasets using 1d convolutional neural networks

## abstract

speech emotion recognition (ser) is a critical component of affective computing, enabling applications in mental health screening, human-computer interaction, and customer service analytics. in this project, we propose a lightweight 1d convolutional neural network (cnn) that classifies emotions from audio using log-mel spectrograms as input features. we evaluate our approach on the ryerson audio-visual database of emotional speech and song (ravdess), an open dataset containing 2452 audio-only files (1440 speech + 1012 song) across eight emotion categories from 24 professional actors. the cnn is compared against a classical baseline using mel-frequency cepstral coefficients (mfcc) combined with a support vector machine (svm). our model targets cpu inference with under 100ms latency and under 5mb model size. the dataset has been downloaded, verified, and split into speaker-disjoint train/val/test partitions. 

> preliminary results on a 20% data subset yield 60.4% accuracy for the svm baseline and 49.1% for the cnn at three training epochs, consistent with expected underfitting at this stage. the full pipeline targets 75-80% weighted accuracy on remaining work covers full training.

all code will be implemented in python with pytorch and designed for cpu inference without specialized hardware.
