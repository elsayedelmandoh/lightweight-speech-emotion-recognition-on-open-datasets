# 01 - motivation & problem

## slide 1: title
- lightweight speech emotion recognition on open datasets: a 1d cnn vs mfcc-svm comparison
- elsayed elmandoh, khaled ashoush, salma essam
- queen's university, cisc 867

## slide 2: what is ser and why it matters
- speech carries paralinguistic info: pitch, tone, energy reveal emotion
- applications: affect-aware assistants, healthcare screening, call center routing, adaptive games
- must run on cpu (laptops, edge devices) -- no gpu assumed

## slide 3: problem statement
- input: ~4s audio clip of acted english speech
- output: 1 of 6 emotions (neutral, calm, happy, sad, angry, fearful)
- constraints: generalize to unseen speakers, infer under 1 ms/sample on cpu
- two approaches: mfcc+svm baseline vs 1d cnn on log-mel-spectrograms

## slide 4: our approach at a glance
- ravdess dataset, speaker-disjoint split (actors 1-19/20-22/23-24)
- svm: gridsearched rbf kernel, c capped at 1 (regularization finding)
- 1d cnn: 132k params, 3 conv1d blocks, log-mel input
- evaluation: test accuracy, per-class recall, latency, confusion matrices

## slide 5: contributions
1. clean reproducible 8-notebook pipeline with strict speaker-disjoint split
2. regularization analysis: capping svm c reduces train-test gap 35pp -> 24pp, improves test accuracy +5pp
3. per-emotion error analysis: fearful easiest (90.6%), neutral hardest (50%)
4. cpu latency benchmarks: both under 1 ms/sample
