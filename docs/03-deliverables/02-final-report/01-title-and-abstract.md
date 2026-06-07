# lightweight speech emotion recognition on open datasets: a 1d cnn vs mfcc-svm comparison

**elsayed elmandoh, khaled ashoush, salma essam**

cisc-867 deep learning course project

---

## abstract

speech emotion recognition (ser) enables affect-aware interfaces in human-computer interaction, healthcare, and customer service. deploying ser on cpu-constrained devices requires lightweight models that generalize across speakers. this paper presents a comparative study of a classical mfcc + svm baseline and a 1d convolutional neural network (cnn) on log-mel-spectrograms for 6-class emotion classification (neutral, calm, happy, sad, angry, fearful) on the ravdess dataset. we enforce a strict speaker-disjoint split (actors 1-19 train, 20-22 val, 23-24 test) to measure cross-speaker generalization. the svm baseline (rbf kernel, c=1) achieves **70.45% test accuracy** and **0.19 ms/sample cpu latency**. the 1d cnn (132,806 parameters) achieves **66.48% test accuracy** and **0.53 ms/sample cpu latency**. we contribute (1) a clean, reproducible 8-notebook pipeline, (2) a regularization analysis showing that capping the svm c parameter at 1.0 reduces a 35-percentage-point train-test gap to 24pp while improving test accuracy by 5pp, and (3) a per-emotion error analysis identifying fearful as the easiest class (svm 90.6%) and neutral as the hardest (50% for both models). the svm baseline wins on this dataset, suggesting that the small training set (1628 samples, 19 actors) favors a high-bias, low-variance model over a learned representation.
