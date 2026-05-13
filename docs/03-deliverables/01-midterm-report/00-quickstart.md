# midterm report - full marks guide

ieee conference format (two-column), 5-8 pages.
template: https://www.ieee.org/conferences/publishing/templates.html

this guide maps each section to what graders expect and what content from our project docs to use. tick every bullet before submitting.

---

## section 1: title and abstract (150-200 words)

**what graders look for:** does the abstract clearly state problem, dataset, method, current status, and contribution in 30 seconds?

**use from our docs:** `01-title-and-abstract.md`

checklist:
- [ ] title mentions lightweight/compact model, ser, and open dataset keywords
- [ ] abstract covers: problem (ser deployment on cpu), dataset (ravdess, 2452 files, 8 emotions), method (1d cnn on mel spectrograms vs mfcc+svm), target constraints (<100ms, <5mb), current status (data acquired and split, preprocessed)
- [ ] abstract is self-contained - readable without the rest of the report
- [ ] word count 150-200 (count it)

---

## section 2: introduction (0.5-1 page)

**what graders look for:** is the problem real? do you know the literature gap? is the scope clear?

**use from our docs:** `02-introduction.md`, `01-problem.md`

checklist:
- [ ] open with a hook: ser applications (healthcare, hci, call centers) and the cpu deployment barrier
- [ ] state the accuracy-efficiency tradeoff clearly: mfcc+svm is fast but inaccurate, 2d cnns are accurate but heavy
- [ ] position 1d cnn as the middle ground
- [ ] cite ravdess dataset + expected accuracy ranges
- [ ] state project scope: 8-class speech emotion + 6-class song on ravdess, cpu target
- [ ] list 3-4 concrete goals (see `02-goal.md`)
- [ ] explicitly state what is out of scope (real-time streaming, multilingual ser)
- [ ] include a problem statement paragraph that a non-expert can understand

---

## section 3: related work (0.5-1 page)

**what graders look for:** do you know the key papers? can you explain how your work differs?

**use from our docs:** `03-related-work.md`

checklist:
- [ ] cover 3-4 papers minimum:
  - [ ] neumann & vu 2017 - attentive cnn, mel vs mfcc, acted vs natural speech
  - [ ] tripathi et al. 2019 - cnn/lstm evaluation, spectral+temporal features
  - [ ] ravdess paper (livingstone & russo 2018) - dataset paper
  - [ ] optional 4th: mfcc+svm baseline paper or ser survey paper
- [ ] for each paper: 2-3 sentence summary + how our project differs/builds
- [ ] identify the gap: "no published work compares 1d cnn vs mfcc+svm on ravdess with cpu deployment constraints"
- [ ] mention reference implementations (marcogdepinto, tuncayka)
- [ ] cite properly in ieee format [1], [2], etc.

---

## section 4: methodology (1-1.5 pages)

**what graders look for:** is the experimental design sound? can someone reproduce it? are the splits correct?

**use from our docs:** `04-methodology.md`, `05-dataset.md`, `06-solution.md`, `08-architecture.md`

checklist:
- [ ] data section:
  - [ ] describe ravdess: 24 actors (12m/12f), 8 speech emotions + 6 song emotions, 2 intensities, 2 statements, 2 repetitions
  - [ ] state total file count: 2452 audio-only (1440 speech + 1012 song)
  - [ ] explain filename convention with a table (modality-channel-emotion-intensity-statement-repetition-actor)
  - [ ] show the 7-part parsing with a concrete example
  - [ ] include a sample waveform or spectrogram figure (eda output)

- [ ] split section:
  - [ ] specify speaker-disjoint split by actor id: train 01-19 (1932 files), val 20-22 (312), test 23-24 (208)
  - [ ] justify why speaker-disjoint (measures cross-speaker generalization, prevents data leakage)
  - [ ] note gender balance is preserved across splits

- [ ] preprocessing section:
  - [ ] describe: silence trimming (top_db=20), amplitude normalization ([-1,1]), fixed-length padding to 3s
  - [ ] state sample rate: 48khz, 16-bit, mono

- [ ] feature extraction section:
  - [ ] mel spectrograms: n_mels=128, n_fft=2048, hop_length=512 -> shape (128, ~282) -> transpose to (282, 128)
  - [ ] mfccs: 40 coefficients + delta + delta-delta, aggregate mean+std -> 240-dim vector

- [ ] model section:
  - [ ] include a diagram of the 1d cnn architecture (3 conv blocks: 64->128->256 channels, kernel=5, batchnorm, pool, dropout)
  - [ ] state parameter count (~200k) and model size (~1mb)
  - [ ] describe svm baseline: rbf kernel, 240-dim mfcc input, grid search c/gamma
  - [ ] mention 3 training scenarios: speech-only 8-class, song-only 6-class, combined 8-class
  - [ ] training config table: adam, lr=1e-3, batch=32, cosine annealing, early stopping, cross-entropy loss

---

## section 5: preliminary experiments and results (~1 page)

**what graders look for:** actual numbers, not just plans. even if nothing is trained yet, show eda results, data statistics, pipeline verification.

**use from our docs:** `05-preliminary-experiments-and-results.md`, and update with **actual** numbers from notebooks

checklist:
- [ ] **critical - replace placeholder text with actual outputs:**
  - [ ] actual file counts by split (we have them: train=1932, val=312, test=208)
  - [ ] actual emotion distribution histogram
  - [ ] actual clip duration histogram (min, max, mean, std)
  - [ ] sample waveforms for 2-3 emotions (angry vs sad vs neutral)
  - [ ] sample mel spectrograms for 2-3 emotions
  - [ ] gender distribution across splits

- [ ] implementation details:
  - [ ] hardware: cpu specs, ram
  - [ ] libraries with versions: python 3.12, librosa, numpy, scikit-learn, pytorch
  - [ ] data loading and caching strategy

- [ ] if any model training started:
  - [ ] training curves (loss vs epoch)
  - [ ] validation accuracy
  - [ ] if not started, state that clearly and explain what is ready

- [ ] include at least 2 figures (no report should be text-only):
  - [ ] figure 1: emotion class distribution
  - [ ] figure 2: sample waveforms or spectrograms and then refer

---

## section 6: planned work and timeline (0.5 page)

**what graders look for:** realistic plan. risks identified. timeline makes sense.

**use from our docs:** `06-planned-work-and-timeline.md`, `11-workflow.md`

checklist:
- [ ] remaining experiments listed with clear goals:
  - [ ] week 3: finalize features, train svm, train cnn, cross-speaker analysis
  - [ ] week 4: ablations, deployment eval, final report
- [ ] risk table with mitigation strategies:

| risk | mitigation |
|------|-----------|
| overfitting on 2452 files | dropout, weight decay, data augmentation |
| poor cross-speaker generalization | speaker-disjoint splits, leave-one-out validation |
| 1d cnn underperforms baseline | fallback to wider network or 2d cnn |
| class imbalance (disgust/surprise from speech only, song missing these) | weighted loss or oversampling |

- [ ] timeline is specific (not just "more training") and references actual notebook numbers

---

## section 7: team contributions

**what graders look for:** each member did real work. roles are clear.

**use from our docs:** `07-team-contributions.md`

checklist:
- [ ] each member has 3-5 bullet points of work already completed
- [ ] each member has 3-5 bullet points of future work
- [ ] contributions are concrete: "parsed 2452 filenames into structured labels" not "worked on data"
- [ ] no overlaps - each member owns distinct deliverables

---

## section 8: references

**what graders look for:** correctly formatted, all cited in text, no missing urls.

**use from our docs:** `08-references.md`

checklist:
- [ ] minimum 4 references, formatted in ieee style:
  ```
  [1] m. neumann and n. t. vu, "title," in proc. interspeech, 2017.
  ```
- [ ] all references cited at least once in the text
- [ ] include the ravdess dataset paper
- [ ] include both main papers
- [ ] include dataset zenodo link
- [ ] no broken urls

---

## formatting checklist (before submission)

- [ ] ieee two-column format
- [ ] 5-8 pages (not shorter, not longer)
- [ ] at least 2 figures
- [ ] at least 1 table
- [ ] section headings numbered (i, ii, iii...)
- [ ] references in [1] [2] format
- [ ] pdf output clean (no weird line breaks, missing fonts)
- [ ] spell-checked
- [ ] all team member names on the report

---

## quick reference: where to find content

| report section | our file |
|---------------|----------|
| title + abstract | `01-title-and-abstract.md` |
| introduction | `02-introduction.md`, `01-problem.md` |
| related work | `03-related-work.md` |
| methodology | `04-methodology.md`, `05-dataset.md`, `06-solution.md`, `08-architecture.md` |
| preliminary results | `05-preliminary-experiments-and-results.md` |
| planned work | `06-planned-work-and-timeline.md`, `11-workflow.md` |
| team contributions | `07-team-contributions.md` |
| references | `08-references.md` |