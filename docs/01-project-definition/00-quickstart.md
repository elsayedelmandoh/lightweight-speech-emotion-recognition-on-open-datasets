# project definition quickstart

use this section to define the project before writing code. keep each file focused on one decision area so the repo stays easy to scan and update.

## 10. Speech Emotion Recognition with 1D CNNs 

### Project Title: Lightweight Speech Emotion Recognition on Open Datasets

### Project Aims & Objectives: 
- Implement a CNN-based model for emotion classification using spectrograms. 
- Compare with classical MFCC + SVM baseline. 
- Evaluate cross-speaker generalization. 
- Optimize for CPU inference. 

### Scope of Work: 
- Use small speech emotion dataset (RAVDESS or CREMA-D). 
- Out of scope: real-time streaming application. 

### Expected Deliverables: 
- Preprocessing pipeline (spectrograms)
- Deep and baseline models
- Performance analysis

### Prerequisite Knowledge / Skills: 
- Basic audio processing (sampling, STFT) 
- CNNs 

### Role of Each Student: 
- Student A: Audio preprocessing and baseline
- Student B: CNN implementation & training
- Student C: Evaluation and report

### Paper(s) Link: 
- Neumann & Vu, “Attentive Convolutional Neural Network based Speech Emotion Recognition: 
A Study on the Impact of Input Features, Signal Length, and Acted Speech,” Interspeech 2017. 
https://arxiv.org/abs/1706.00612 

- Tripathi et al., “Deep Neural Networks for Emotion Recognition in Speech,” IJCNN 2019. 
https://doi.org/10.1109/IJCNN.2019.8852153 

### Data Link: 
- RAVDESS: https://zenodo.org/record/1188976 

### Code Link (reference): 
- Example SER repo: https://github.com/marcogdepinto/emotion-recognition-english 

### Timeline: 
- Week 1: Understand data; preprocess
- Week 2: Baseline; CNN; midterm report
- Week 3: Training; cross-speaker experiments
- Week 4: Finalization