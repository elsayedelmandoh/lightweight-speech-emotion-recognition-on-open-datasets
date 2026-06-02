# Lightweight Speech Emotion Recognition on Open Datasets Using 1D Convolutional Neural Networks 

Elsayed Elmandoua 
Department: AI & Data Science  

Salma Essam 
Department: Department: AI & Data Science 

Khaled  Ahmed 
Department: Department: AI & Data Science 

## 1. Abstract 
### 1.1 Problem: Speech Emotion Recognition (SER) is a critical 
component of affective computing, enabling applications in mental health screening, human-computer interaction, and customer service analytics. Accurately classifying human emotions from raw audio remains a challenging task due to inter-speaker variability, class imbalance, and the need for lightweight models suitable for CPU-only deployment.  

### 1.2 Dataset: Our model is evaluated on the Ryerson Audio-Visual 
Database of Emotional Speech and Song (RAVDESS), an open dataset comprising 2,452 audio-only recordings (1,440 speech and 1,012 song) spanning eight emotion categories performed by 24 professional actors. The dataset has been downloaded, verified, and partitioned into speaker-disjoint training, validation, and test splits to ensure cross-speaker generalization.  

### 1.3 Model Idea: We propose a lightweight one-dimensional 
Convolutional Neural Network (1D CNN) that classifies emotions from audio recordings using Log-Mel Spectrograms as input features. The proposed CNN is benchmarked against a classical baseline combining Mel-Frequency Cepstral Coefficients (MFCCs) with a Support Vector Machine (SVM). The architecture is designed for CPUonly inference, targeting under 100ms latency and under 5MB model size.  

### 1.4 Current Status: Preliminary experiments on a 20% data 
subset yield 56.4% accuracy for the SVM baseline and 49.1% for the CNN at three training epochs, consistent with expected underfitting at this early stage. Remaining work focuses on full-scale training, hyperparameter tuning, and cross-speaker evaluation.

## 2. INTRODUCTION 
### A. Problem Statement 
Human speech carries rich paralinguistic information beyond lexical content; prosody, rhythm, and spectral characteristics encode a speaker’s emotional state in ways that are both computationally accessible and practically valuable. Robust emotion recognition from speech remains an open problem, complicated by speaker variability, cultural differences in expression, and the inherent ambiguity of affective labels. The core tension in SER is between accuracy and efficiency. Classical methods such as MFCC features with SVM classifiers are lightweight but achieve modest accuracy  on RAVDESS (50– 65%) because they fail to capture the temporal and spectral dynamics of emotional speech. Conversely, deep learning models including 2D CNNs achieve higher accuracy but are often over-parameterized for the task, making deployment on CPU-only environments impractical. 
 
### B. Motivation 
There is a clear need for SER models that occupy the middle ground: architectures that leverage the pattern-recognition capabilities of convolutional networks while remaining small enough for CPU inference. 1D CNNs offer a promising direction because they operate directly on the time axis of mel spectrograms with frequency bands as input channels, requiring far fewer parameters than 2D CNNs that treat spectrograms as images [2]. Additionally, the RAVDESS dataset includes both speech and song recordings, enabling investigation of crosschannel generalization — a relatively underexplored question in SER literature. 

### C. Project Scope 
This project focuses on: 
• Implementing a 1D CNN for emotion classification on RAVDESS across three scenarios: speech-only (8-class, 1,440 files), song-only (6-class, 1,012 files), and combined (8-class, 2,452 files). 
• Building an MFCC + SVM baseline for direct comparison on all scenarios. 
• Evaluating cross-speaker generalization using speakerdisjoint train/val/test splits (Train: Actors 1–18, Val: 19– 21, Test: 22–24). 
• Measuring cross-channel generalization: train on speech, test on song and vice versa. 
• Optimizing for CPU inference (target: <100ms per clip, <5MB model size). Explicitly out of scope: real-time streaming inference, multilingual SER, and continuous arousal-valence prediction. 

### D. Goals 
1) Demonstrate that a 1D CNN on Log-Mel Spectrograms outperforms the MFCC + SVM baseline by at least 10 percentage points on speaker-disjoint test splits across multiple scenarios. 
2) Achieve ≥70% test accuracy on speech 8-class and ≥65% on song 6-class. 
3) Evaluate cross-channel generalization between speech and song. 
4) Produce a deployable model that runs on a single CPU core within latency and size budgets. 
5) Document reproducible training and evaluation pipelines from raw WAVs to final results. 

## 3. RELATED WORK 
Over the last twenty years, Speech Emotion Recognition 
(SER) has undergone considerable change from the traditional 
hand extracted features to an all in one solution using deep 
learning techniques. This section will begin with an overview 
of representative prior research related to building datasets, 
traditional methods, and contemporary neural methods. We 
will then articulate how we have leveraged and advanced 
previous research. 
 
### A. The RAVDESS Dataset 
Livingstone and Russo [1] introduced RAVDESS, an 
audiovisual database comprising 1,440 speech recordings 
from 24 professional North American English-speaking actors 
(12 male, 12 female) across eight emotional categories: 
neutral, calm, happy, sad, angry, fearful, disgusted, and 
surprised. Emotional validity was established through 
perceptual ratings from 247 raters. The dataset is publicly 
available via Zenodo [2]. In our work, RAVDESS is evaluated 
under a strict speakerindependent split to assess cross-
speaker generalization, a critical requirement for real-world 
SER deployment. 
 
### B. Classical Feature-Based Approaches 
Prior to deep learning, SER systems relied on hand-crafted 
acoustic features paired with traditional classifiers. The MFCC 
+ SVM pipeline was widely adopted due to its low memory 
consumption, fast inference, and competitive benchmark 
performance. However, hand-crafted features are inherently 
limited in their capacity to capture complex spectro-temporal 
emotional patterns. In this work, we implement the MFCC + 
SVM pipeline as our classical baseline to quantify the 
performance 
gain 
achieved 
through 
learned 
deep 
representations. 
 
### C. Deep Learning Approaches for SER 
Attentive CNN — Neumann & Vu (2017). Neumann and Vu 
[3] proposed an Attentive Convolutional Neural Network 
(ACNN) for SER, conducting a systematic evaluation of three 
key factors affecting recognition performance: 
• Input Feature Type: Log Mel Spectrograms consistently 
outperform raw MFCCs as CNN inputs, owing to their 
logarithmic compression of mel-scaled frequency bands, 
which more closely mirrors the non-linear loudness 
perception of the human auditory system. 
• Signal Length: Standardizing audio clips to a fixed 
duration produces more stable training dynamics. 
Segments of approximately three seconds provide 
sufficient temporal context for reliable emotion 
modeling. 
• Acted vs. Natural Speech: A significant performance drop 
was observed when crossing speech style boundaries 
between acted (RAVDESS) and natural conversational 
speech(IEMOCAP),identifying cross-speaker generalization 
as a key challenge we adopt Log-mel  Spectrograms (128 mel 
filterbanks,N_FFT=1024, HOP_LENGTH=512, SR=16KHz 
) as our primary CNN input, standardize all clips to exactly 3 
seconds via zero-padding or truncation, and apply per-file 
standardization (zero mean, unit variance) to account for 
speaker-level loudness variability. We deliberately exclude 
the attention mechanism, opting instead for a lightweight 3-
block CNN with filter sizes [64, 128, 256] designed for CPU-
only inference. Additionally, we enforce a strict speaker-
independent split of 18/3/3 actors to explicitly evaluate cross-
speaker generalization. 

### D. Deep Neural Networks for SER 
Tripathi et al. (2019). Tripathi et al. [4] present a 
comprehensive comparison of CNN, LSTM, and hybrid 
CNNLSTM architectures for SER using spectrogram-based 
inputs, yielding the following key findings: 
• CNNs applied to 2D spectrogram representations achieve 
strong classification accuracy by learning spatially local 
spectro-temporal 
emotional 
patterns 
through 
hierarchical convolutional feature extraction. 
• LSTMs capture long-range temporal dependencies in 
sequential speech features but incur significantly higher 
computational cost, making them unsuitable for 
resourceconstrained deployment. 
• CNN-LSTM Hybrids combine the spatial feature extraction 
of CNNs with the temporal modeling of LSTMs, achieving 
the highest classification accuracy at the cost of greater 
model complexity, memory footprint, and inference 
latency. 
• Cross-Speaker Evaluation: A significant performance gap 
was observed between same-speaker and crossspeaker 
conditions, confirming that random data splits produce 
artificially inflated accuracy figures that do not reflect 
real-world generalization. 

### Relation to Our Work: We adopt Tripathi et al.’s CNNon- 
spectrogram paradigm, substituting standard spectrograms 
with Log Mel Spectrograms as motivated by Neumann and Vu 
[3]. Our architecture is constrained to a lightweight 3-block 
CNN with filter depths [64, 128, 256], Batch Normalization, 
and a single Dropout (0.4) layer within the fully connected 
classifier, driven by our CPUonly hardware constraint. Training 
uses the Adam optimizer (lr=0.001, batch size=32, NUM_ 
EPOCHS = 50) with early stopping and learning rate reduction on plateau. We further address RAVDESS class imbalance via class-weighted cross-entropy loss. Critically, motivated by 
their finding on random split unreliability, we enforce a strict 
speaker-independent split of 18/3/3 actors, ensuring no test-
set speaker appears during training or validation. 

### 4. METHODOLOGY 
### A. Dataset Description 
All experiments described in this paper are carried out on 
the Ryerson Audio-Visual Database of Emotional Speech and 
Song (RAVDESS) [1]. The RAVDESS database consists of a total 
of 2,452 recordings, split into two modalities, speech (1,440, 
58.7%) and song (1,012, 41.3%), and was recorded by 24 
professional actors from North America (12 male, 12 female). 
Each recording presents one of eight different emotional 
expressions: Neutral, Calm, Happy, Sad, Angry, Fearful, Disgust 
and Surprised. As seen in Figure 1, the corpus has a moderate 
level of class imbalance whereby the emotions of Disgust, 
Surprised and Neutral have about half as many samples as the 
other five classes (192 vs. 376 recordings per class across 
modalities). It should also be noted that the Song modality has 
no recordings for either Disgust or Surprised, which creates 
and accentuates further imbalance. The distributional skew is 
a significant challenge and is specifically addressed in our 
training strategy (see Section III-G). All recordings are sampled 
at 48,000 Hz with a range of utterance lengths being between 
2.94 and 6.37 seconds with a mean length of 4.09 seconds for 
the entire corpus. 
 
Fig. 1. RAVDESS overview: emo- Fig. Duration distribution, 
speech-to-song (mean=4.09s), duration per emoratio, gender 
balance, intensity distrubtion, files per actor, speech vs. song. 
The chart in Fig.2 helps to visualise the overall distribution of 
recording durations throughout the corpus (utterance lengths 
range from 2.94 to 6.37 sec, average 4.09 sec) and supports 
the conclusion that most recordings were within the range of 
3.5 to 4.5 seconds. The data are equally represented across 
both genders for each emotion category. 

### B. Data Splitting Strategy 
To ensure that the reported performance metrics reflect true 
cross-speaker generalization rather than the memorization of 
speaker-specific characteristics, a strict speaker-independent 
split is enforced across all experiments. The 24 actors are 
partitioned as follows: Actors 1–18 (18 actors) are assigned to 
the training set; Actors 19–21 (3 actors) are assigned to the 
validation set; and Actors 22–24 (3 actors) form the heldout test 
set. Zero overlap at the speaker level across all splits was 
verified programmatically via set intersection checks. The 
resulting split sizes are summarized in Table I. 
SPEAKER-INDEPENDENT DATA SPLIT 
Split 
Files 
Actors 
% 
Train 1,828 
1–18 
74.5% 
Val 
312 
19–21 
12.7% 
Test 
312 
22–24 
12.7% 
Total 2,452 
24 
100% 
Train∩Val=0, Train∩Test=0, Val∩Test=0 
This design is motivated by prior findings [4] demonstrating 
that random splitting strategies which permit utterances from 
the same speaker to appear in both training and test sets yield 
artificially inflated accuracy estimates that fail to generalize to 
previously unseen speakers in real-world deployment 
conditions. 

### C. Audio Preprocessing Pipeline 
All sound files go through the same 4-step process before 
feature extraction, as illustrated in Fig. 3. 
 
Fig. 3. Four-stage preprocessing pipeline:  
1- Raw audio (48kHz, 4.24s);  
2- resampled to 16kHz; 
 3- silence trimmed (2.21s);  
4- normalized + fixed 3.0s. 
1) Resampling: Each recording is down-sampled from 
48,000 Hz to 16,000 Hz. The majority of acoustic cues of 
emotion in speech are located below 8,000 Hz (Nyquist-
Shannon theorem), so 16,000 Hz is sufficient and 
decreases sample count by 67%. 
2) Silence Trimming—Leading and trailing silence below the 20 dB threshold is removed to focus the model on acoustically meaningful content and eliminate recording artefacts. 
3) Amplitude Normalisation Each waveform is normalized 
by its maximum absolute amplitude to the range [−1,+1], 
removing inter-speaker loudness variability. 
4) Fixed-Length Standardisation All recordings are fixed to 
3.0 seconds (48,000 samples at 16,000 Hz). Shorter clips 
are zero-padded; longer ones are centrecropped to ensure 
consistent batch dimensions. 

### D. Feature Extraction 
To support the two modeling approaches evaluated in this 
study, two complementary feature representations are extracted 
as follows: 1) Log-Mel Spectrogram (for 1D CNN). The 
primary input is a Log-Mel Spectrogram with Nmels = 128 mel 
filterbanks, NFFT = 1024 samples, and hop length of 512 
samples, yielding a feature map of shape (128 × 94). The power 
spectrogram is converted to dB via librosa.power_to_db, then 
normalized to zero mean and unit variance per sample. As 
illustrated in Fig. 4, the LogMel representation captures distinct 
spectro-temporal patterns across all 8 emotion classes, with 
high-arousal emotions (anger, happiness) showing elevated 
energy across broad frequency ranges, while low-arousal 
emotions (sadness, calmness, neutrality) exhibit concentrated 
lower-frequency activity. 
2) MFCC Feature Vector (for SVM Baseline). 40 MFCCs are 
extracted from each preprocessed wavefile. Four summary 
statistics (MEAN(40), STD(40), MIN(40), MAX(40)) per 
coefficient yield a 4 × 40 = 160-dimensional feature vector per 
recording, suitable for SVM classification. 
 
Fig. 4. MFCC (left) vs Log-Mel Spectrogram (right) for all eight 
emotion classes. High-arousal emotions show elevated broad-
band energy; low-arousal emotions show concentrated lower-
frequency activity. 

### E. Model Architecture 
The proposed model is a three-block 1D CNN processing 
Log-Mel Spectrograms as multi-channel sequential signals. 
Input tensor shape: (batch×128×94), where 128=mel 
channels, 94=temporal frames. Each convolutional block 
follows: 
Conv1d→BatchNorm1d→ReLU→MaxPool1d(2) 
Filters increase as [64 → 128 → 256] with kernel size 3 and 
same-padding. A Global Average Pooling layer 
(AdaptiveAvgPool1d(1)) collapses the temporal dimension to 
a 256-D vector, passed to a two-layer fully connected classifier 
with Dropout(0.4). Table II summarizes the full architecture. 
 
1D CNN ARCHITECTURE SUMMARY 
Layer 
Output 
Params 
Midterm 
(done) 
Data, 
EDA, 
preprocessing, 
midterm report 
Split 
data, 
split_labels.csv, 
this report 
Phase A 
Feature 
extraction 
.npy arrays for 2,452 
clips 
Phase B 
SVM+CNN 
training 
Models, curves, met- 
rics 
Phase C 
Cross-channel, 
ablation 
Accuracy 
table, 
ablation results 
Phase D 
Deployment, 
final report 
Model export, PDF, 
slides 
 
Layer 
Output 
Params 
Input 
(B,128,94) 
--- 
Conv1d(128→64) 
(B,64,94) 
24,640 
BN+ReLU+Pool 
(B,64,47) 
128 
Conv1d(64→128) 
(B,128,47) 
24,704 
BN+ReLU+Pool 
(B,128,23) 
256 
Conv1d(128→256) 
(B,256,23) 
98,560 
BN+ReLU+GAP 
(B,256,1) 
512 
Flatten 
(B,256) 
------ 
Linear(256→128) 
(B,128) 
32,896 
Dropout(0.4) 
(B,128) 
------- 
Linear(128→8) 
(B,8) 
1,032 
Total Params 
 
182,728 
 
The architecture is lightweight (≈182,728 parameters), 
operating entirely on CPU without GPU acceleration. 

### F. Baseline Model: MFCC + SVM 
The classical baseline is an SVM with RBF kernel trained on 
160-dimensional MFCC feature vectors. Features were 
standardized using StandardScaler fitted on training data only 
(preventing data leakage). The SVM was configured with C = 
10, gamma=‘scale’, and class_weight=‘balanced’ to address 
class imbalance. Implementation used scikit-learn. 

### G. Training Configuration and Expected Challenges 
Training used Adam (lr=0.001, weight decay=10−4), batch 
size 32, maximum 50 epochs. Two primary challenges were 
addressed:  


#### Challenge 1: Class Imbalance. As noted in Section IV-A, 
Disgust, Surprised, and Neutral contain approximately half the 
samples of other classes. Class-weighted crossentropy loss 
was applied, with weights inversely proportional to class 
frequency in the training set, penalizing minority class 
misclassifications more severely.  

#### Challenge 2: Overfitting. Preliminary experiments revealed 
a generalization gap: training accuracy >95% vs. validation 
accuracy 62–65%. Four strategies were employed: 
• Dropout (0.4): Suppresses neuron co-adaptation in the 
classifier. 
• Batch Normalization: Applied after each convolutional 
layer 
for 
activation 
stabilization 
and 
implicit 
regularization. 
• Early Stopping: Training halts after 10 patience epochs of 
no validation loss improvement; best checkpoint is 
restored. 
• ReduceLROnPlateau: Learning rate halved after 5 epochs 
of stagnating validation loss. 
 
## 5. PRELIMINARY EXPERIMENTS AND RESULTS 
### A. Current Status 
As of the midterm checkpoint, we have completed the full 
sample-based pipeline: data acquisition, exploratory data 
analysis, preprocessing, feature engineering, and an initial 
MFCC + SVM baseline run on a representative subset (416 
files, 17% of the full dataset). All 7 notebooks in notebooks/00-
preliminary-experiments/ have been executed end-to-end. 
 
### B. Dataset Overview (Sample Subset) 
SAMPLE SUBSET SPLIT 
Split 
Actors 
Speech Song 
Total 
Train 
01,02 
120 
88 
208 
Val 
20 
60 
44 
104 
Test 
23 
60 
44 
104 
Total 
4 
240 
176 
416 
104 files per actor per channel. Actors chosen to cover both    
genders and all three splits. 

### C. Preprocessing Metrics 
PREPROCESSING METRICS 
Step 
Result 
Load+trim+normalize 
416 clips, 14.9s (35.9ms/clip) 
Typical trim reduction 
4.40s→2.36s 
Final clip length 
3.00s (48,000 samples at 16kHz) 
Amplitude normalization [−1,+1] range verified 
 
 
 
 
### D. Feature Extraction 
FEATURE EXTRACTION SUMMARY 
Feature 
Shape/clip Total time 
Log-Mel Spectrogram 
(128, 94) 
∼8s 
MFCC *4 stats (min, max 
,mean, std) 
(160-dim) 
∼50s (416 
files) 
 
### E. MFCC + SVM Baseline Results 
Trained on 208 clips (Actors 01–02), tested on 104 clips 
(held-out Actor 23). 
BASELINE OVERALL 
Metric 
Test(Actor) 
Test Accuracy 
27.9% (29/104) 
Macro F1 
0.238 
Weighted F1 
0.260 
Random chance (8-class) 
12.5% 
Improvement over chance  
2.2× 
Feature extraction 
25.0s for 208 clips 
SVM training 
0.016s 
Inference (single) 
0.425ms 
Inference (batch 32) 
1.796ms (0.056ms/clip) 
Model size 
412 KB 
 
#### 1) Overall Metrics: 
SVM BASELINE PER CLASS 
Emotion 
F1 
Acc. 
Confused with 
Neutral 
0.222 12% 
Fearful 
Calm 
0.400 44% 
Surprised 
Happy 
0.467 44% 
Angry 
Sad 
0.000 0% 
Surprised 
Angry 
0.400 44% 
Happy 
Fearful 
0.207 19% 
Calm 
Disgust 
0.000 0% 
Surprised 
Surprised 0.205 50% 
Angry 
 
#### 2) Per-Class Analysis: 
SVM BASELINE—PER-CHANNEL 
Channel 
Accuracy 
Count 
Speech 
18.3% (11/60) 
Actor 23 speaking 
Song 
40.9% (18/44) Actor 23 singing 
 
#### 3) Per-Channel Analysis: Song performs better than speech. 
Hypothesis: song has more sustained, exaggerated vocal 
patterns that are easier to distinguish. 
 
 
 


SVM BASELINE—PER-INTENSITY 
Intensity 
Accuracy 
Count 
Normal 
23.2% (13/56) 
Strong 
33.3% (16/48) 
 
#### 4)Per-Intensity Analysis: Strong intensity yields higher 
accuracy, consistent with the expectation that exaggerated 
emotions are easier to classify. 

#### 5)Confusion Patterns: The normalized confusion matrix 
reveals: 
• Sad (0% accuracy) is almost never predicted correctly, 
most often confused with Surprised and Calm. 
• Disgust (0%) is also never correctly identified, primarily 
classified as Surprised. 
• Surprised has the highest per-class accuracy (50%) but is 
also the most common false prediction. 
• High-arousal emotions (Angry, Happy) are mutually 
confusable, as are low-arousal emotions (Calm, Sad, 
Neutral). 
These patterns are expected when training on only 2 actors. 
With 19 training actors, the model will learn more robust 
emotion-specific features and reduce these confusions. 

### F. Implementation Details 
IMPLEMENTATION DETAILS 
Component 
Detail 
Language 
Python 3.12.13 
Audio loading 
librosa 0.11.0 
Machine learning scikit-learn 1.8.0 
Data handling 
NumPy, Pandas 
Visualization 
Matplotlib, Seaborn 
Model persistence 
joblib 
Environment 
Conda on WSL2 (Ubuntu) 
Hardware 
4 CPU cores, 8.3 GB RAM 
Pipeline 
t-tracked Jupyter Notebooks 
 
## 6. PLANNED WORK AND TIMELINE 
### A. Remaining Experiments 
#### 1) Phase A: Feature Engineering (Notebook 04): 
##### 1) Log-Mel Spectrograms for CNN 
• Input: trimmed WAVs 
from data/{train,val,test}/ 
{speech,song}/ 
• Compute log-mel spectrogram (n mels=128, n 
fft=1024, hop length=512) 
• Output shape: (128, 94)→ save as .npy arrays 
• Separate files for speech (1,440), song (1,012), 
combined (2,452) 

##### 2) MFCC Vectors for SVM 
• Extract 40 MFCCs 
• Aggregate as mean, std, min, max→40*4 = 160-dim 

##### 3) Save Label Arrays 
• Emotion class ints for each clip 
• One-hot optional for CNN training 

#### 2) Phase B: Model Training (Notebook 05): 
##### 4) Train SVM Baseline 
• Speech-only 8-class: 1,140 files 
• Song-only 6-class: 792 files 
• Combined 8-class: 1,932 files 
• Grid search C=[0.1,1,10,100] 

##### 5) Train 1D CNN 
• 3-block PyTorch architecture • Adam (lr=10−3), 
batch=32 
• Early stopping (patience=10) 

##### 6) Cross-Speaker Analysis 
• Per-speaker accuracy (Actors 23–24) 
• Gender+intensity breakdown 

#### 3) Phase C: Cross-Channel and Ablation (Notebook 06): 
##### 7) Cross-Channel Experiments 
• Train on speech, test on song 
• Train on song, test on speech 
• Report accuracy degradation  

##### 8) Ablation Experiments 
• Vary n mels: [64, 128, 256] 
• Vary conv blocks: [2, 3, 4]  
• With/without BatchNorm, Dropout  
 
#### 4) Phase D: Deployment (Notebook 07): 
##### 9) Deployment Evaluation 
• CPU inference latency+model size 
• Export as TorchScript 

##### 10) Final Report and Presentation 
• IEEE-format final report 
• Presentation slides 

### B. Risks and Mitigation 
TABLE XI 
RISKS AND MITIGATION 
Risk 
Like. Imp. Mitigation 
Overfitting 
High 
High Dropout, weight 
decay, 
early 
stopping 
Poor- cross speaker 
Med. High Speaker-disjoint
splits; 


per-speaker 
results 
CNN<SVM 
Low 
High Wider CNN (512 
ch); 
4th 
conv 
block 
Class imbalance 
Med. Med. Weighted loss; 
per-class F1 
Song<Speech Med. 
Med. Expected; cross 
channel 
inherently harder 
 
### C. Timeline 
PROJECT TIMELINE 
Phase Tasks Deliverables 

Midterm (done) Data, EDA, 
preprocessing, 
midterm report 
Split 
data, 
split_labels.csv, 
this report 

#### Phase A 
Feature 
extraction 
.npy arrays for 2,452 
clips 

#### Phase B 
SVM+CNN 
training 
Models, curves, met- 
rics 

#### Phase C 
Cross-channel, 
ablation 
Accuracy 
table, 
ablation results 

#### Phase D 
Deployment, 
final report 
Model export, PDF, 
slides 
 
## 7. TEAM CONTRIBUTIONS 
### A. Elsayed—Audio Preprocessing and Baseline 
#### 1) Completed: 
• Downloaded and verified RAVDESS dataset (1440 audio 
files). 
• Built filename parser to extract emotion, intensity, 
statement, repetition, actor, and gender labels. 
• Implemented preprocessing pipeline: silence trimming, 
amplitude normalization, fixed-length padding. 
• Ran exploratory data analysis: class distribution, clip 
durations, waveform and spectrogram visualization. 
#### 2) Planned: 
• Finalize MFCC feature extraction pipeline. 
• Implement and train SVM baseline with grid search. 
• Implement data augmentation (time shift, noise injection, 
speed perturbation). 

### B. Salma—CNN Implementation and Training 
#### 1) Completed: 
• Designed 1D CNN architecture (3 conv blocks, global 
average pooling, fully connected head). 
• Implemented log-mel spectrogram extraction prototype. 
• Verified feature shapes and caching pipeline. 
#### 2) Planned: 
• Implement full CNN training loop in PyTorch (loss, 
optimizer, scheduler, early stopping). 
• Run training experiments with hyperparameter tuning. 
• Run ablation experiments (number of mel bands, conv 
blocks, regularization). 

### C. Khaled—Evaluation and Report 
#### 1) Completed: 
• Defined evaluation metrics: accuracy, per-class F1, 
confusion matrix, latency, model size. 
• Set up speaker-disjoint train/validation/test split (Actors 
1–18/19–21/22–24). 
• Drafted midterm report. 
#### 2) Planned: 
• Run full evaluation on test set for both CNN and SVM. 
• Cross-speaker analysis: per-speaker accuracy, gender 
breakdown, intensity comparison. 
• Measure inference latency and model size for 
deployment report. 
• Compile final report and presentation. 

## 8. REFERENCES 
[1] S. R. Livingstone and F. A. Russo, “The Ryerson Audio-
Visual Database of Emotional Speech and Song 
(RAVDESS),” PLOS ONE, vol. 13, no. 5, p. e0196391, 
2018. 
[2] S. R. Livingstone and F. A. Russo, “RAVDESS Dataset,” 
Zenodo, 2018. doi: 10.5281/zenodo.1188976 
[3] M. Neumann and N. Q. K. Vu, “Attentive Convolutional 
Neural Network based Speech Emotion Recognition,” 
arXiv preprint arXiv:1706.00612, 2017. 
[4] S. Tripathi et al., “Deep Neural Networks for Emotion 
Recognition in Speech,” in Proc. IJCNN, 2019. 
 
## 9.Use of GenAI Tools 
GenAI tools (Claude / ChatGPT) were used in limited 
capacities for this project. Specifically, they were used to 
(1) correct grammar and phrasing in the written report 
(2) Clarify the documentation of the Python libraries used 
(librosa, scikit-learn), 
(3) Assist with debugging after initial self-directed 
attempts. No end-to-end code was generated through 
GenAI and no report sections, experimental results, or 
figures were generated by generative AI. All model 
design choices, experimental choices, and written analysis 
are the team's own.  
