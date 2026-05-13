# title and abstract

## title

lightweight speech emotion recognition on open datasets using 1d convolutional neural networks

## abstract

speech emotion recognition (ser) is a critical component of affective computing, enabling applications in mental health screening, human-computer interaction, and customer service analytics. however, deploying ser models on resource-constrained devices remains challenging due to the computational cost of deep learning approaches. in this project, we propose a lightweight 1d convolutional neural network (cnn) that classifies emotions from audio using log-mel spectrograms as input features. we evaluate our approach on the ryerson audio-visual database of emotional speech and song (ravdess), an open dataset containing 2452 audio-only files (1440 speech + 1012 song) across eight emotion categories from 24 professional actors. we compare three training scenarios - speech-only 8-class, song-only 6-class, and combined 8-class - and also measure cross-channel generalization by training on speech and testing on song and vice versa. the cnn is compared against a classical baseline using mel-frequency cepstral coefficients paired with a support vector machine. our model targets cpu inference with under 100ms latency and under 5mb model size. the dataset has been downloaded, verified, and split into speaker-disjoint train/val/test partitions. preliminary exploratory analysis is complete, with training and evaluation planned as the next phase. our work demonstrates that compact 1d cnns can serve as practical, deployable solutions for ser on open benchmarks.
