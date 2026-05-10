# problem statement

speech emotion recognition (ser) remains unreliable in real-world conditions. most existing approaches either rely on large, computationally expensive models or fail to generalize across speakers and recording environments. lightweight, accurate ser on open datasets is an unsolved challenge.

## user pain

- emotion-aware applications (call centers, mental health screening, human-robot interaction) need ser models that run on cpu/edge devices without gpu infrastructure.
- current lightweight baselines (mfcc + svm) achieve modest accuracy and do not capture temporal patterns in speech.
- deep learning approaches (cnns, lstms) perform better but are often over-parameterized for the task, making deployment impractical on resource-constrained hardware.

## current workaround

- practitioners either accept low accuracy from classical methods or deploy large models that require gpu inference.
- no widely-adopted lightweight ser model balances accuracy and inference cost on open benchmark datasets.

## why now

- open datasets like ravdess make reproducible research possible without proprietary data.
- 1d cnns on spectrograms offer a middle ground: they capture local temporal/frequency patterns with far fewer parameters than 2d cnns or transformer-based models.
- cpu inference is a hard requirement for real-world deployment scenarios (embedded, mobile, web api).
