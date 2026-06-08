## 1. introduction

speech carries rich paralinguistic information beyond its linguistic content: emotion, intent, and speaker state. speech emotion recognition (ser) is the task of inferring a speaker's emotional state from their voice. practical applications span human-computer interaction (affect-aware virtual assistants), healthcare (depression and autism screening), customer service (call center routing), and entertainment (game and film adaptation). the ravdess dataset [1] is widely used for ser research because it provides acted emotional speech and song from 24 north american english speakers across 8 emotion categories (calm, happy, sad, angry, fearful, surprise, disgust, neutral).

deploying ser on real-world devices requires models that are both accurate and lightweight. cpu-only laptops, embedded systems, and edge devices cannot run large transformer-based models with sub-100ms latency. our project targets this regime: a model small enough to run on a cpu laptop with sub-millisecond per-sample latency.

**problem statement.** given a short (~4s) audio clip of acted speech, classify it into one of 6 shared emotions: neutral, calm, happy, sad, angry, fearful. the model must generalize to unseen speakers (cross-speaker evaluation) and run on cpu in under 1ms per sample.

**project scope.**
- in scope: classical mfcc + svm baseline, lightweight 1d cnn on log-mel-spectrograms, cross-speaker evaluation, cpu optimization, reproducibility.
- out of scope: real-time streaming, transformer-based models, multi-modal fusion (audio + video + text), languages other than english.

**contributions.**
1. we implement a clean two-model comparison: a classical mfcc + svm baseline and a 1d cnn on log-mel-spectrograms, both in a single reproducible pipeline.
2. we design a strict speaker-disjoint split (actors 1-19/20-22/23-24) and verify cross-speaker generalization on held-out actors 23-24.
3. we contribute a regularization analysis: capping the svm c parameter at {0.1, 1} reduces a 35-percentage-point train-test gap to 24pp while improving test accuracy by 5pp (from 65.34% to 70.45%).
4. we ship cpu-latency measurements (svm 0.19 ms/sample, cnn 0.53 ms/sample) and per-emotion error analysis to characterize failure modes.

**outline.** section 2 reviews related work. section 3 describes the data and preprocessing pipeline. section 4 details the model architectures and training procedure. section 5 presents experiments and results. section 6 discusses strengths, weaknesses, and limitations. section 7 concludes.
