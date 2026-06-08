# project definition quickstart

## General Structure for All Projects

- Teams: 3 students
- Duration: 4 weeks
- Deliverables (common)
    - Midterm report (IEEE-style, ~4 pages) – end of Week 3
    - Final report (IEEE-style, ~6–8 pages) – end of Week 6
    - 20-minute presentation + 5–10 minutes Q&A
    - GitHub repository with:
        - Code
        - README.md (problem, method, data, how to run)
        - Reproducible experiments (scripts, seeds, configs)

- Grading emphasis: Reproducibility, understanding, and incremental originality (ablation, small extension, or strong analysis). Aim for publishable quality.

- Hardware/software assumptions:
    - CPU laptop with ≥8 GB RAM (no GPU assumed)
    - Python 3.9+; PyTorch or TensorFlow + common libraries (NumPy, Pandas, scikit-learn, Matplotlib/Seaborn, Jupyter)
---


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
---


## midterm report template (IEEE-style, ~5-8 pages) 

Use IEEE conference format (two-column). 

Template: https://www.ieee.org/conferences/publishing/templates.html 

### Sections: 
#### 1.  Title and Abstract (150–200 words) 
- problem
- dataset
- model idea
- current status

#### 2.  Introduction (0.5–1 page) 
- problem statement
- motivation
- project scope 
- goals

#### 3.  Related Work (0.5–1 page) 
- 2–4 key papers
- How your project builds on them / differs

#### 4.  Methodology (1–1.5 pages) 
- Data description (source, preprocessing)
- Model architecture(s) (diagrams encouraged) 
- Baselines you plan to implement

#### 5.  Preliminary Experiments and Results (~1 page) 
- Any initial training runs, metrics on small subset
- Implementation details (hardware, libraries)

#### 6.  Planned Work and Timeline (0.5 page) 
- Remaining experiments, ablations
- Risks and mitigation strategies

#### 7.  Team Contributions 
- Bullet list of each member’s work so far and future responsibilities

#### 8.  References
---


## final report template (IEEE-style, ~10–15 pages)

same IEEE format: 

### 1.  Title and Abstract 
- Summarize problem, method, results, and contributions

### 2.  Introduction 
- Background and real-world relevance
- Clear problem definition
- Contributions (e.g., “We reproduce X, propose Y extension, and analyze Z”)

### 3.  Related Work 
- 5–10 key references
- Compare methods conceptually

### 4.  Data and Preprocessing 
- Dataset details (size, splits, sources, licenses)
- Preprocessing steps (filters, tokenization, normalization)
- Train/validation/test setup

### 5.  Methodology 
- Model architectures (with diagrams if possible)
- Training procedure (losses, learning rates, optimizers, epochs, batch sizes)
- Baselines and ablations

### 6.  Experiments and Results 
- Quantitative results (tables, figures)
- Comparison with baselines and/or reported numbers from papers
- Efficiency (runtime, memory) where relevant
- Ablation studies (e.g., without augmentation, smaller model)

### 7.  Discussion 
- Interpretation of results; strengths and weaknesses. 
- Error analysis and failure cases
- Limitations and future work (including what would be needed for publication)

### 8.  Conclusion 
- Key takeaways
- Potential impact or next steps

### 9.  Team Contributions 
- Clear breakdown per student (design, coding, experiments, writing)

### 10. References 

### 11. Appendix (optional) 
- Extra figures, hyperparameter tables, additional results
---

## Presentation Requirements (20 minutes)

### Recommended structure:

#### 1. Motivation & Problem (3–4 min)

#### 2. Data & Method (6–7 min)

#### 3. Results & Analysis (6–7 min)

#### 4. Limitations & Future Work (2–3 min)

> All team members must speak.
---

## General Grading Rubric (100 points)

### 1. Technical Depth & Correctness (30 pts)
- Accurate implementation of models and baselines (10)
- Proper experimental protocol (splits, metrics, reproducibility) (10)
- Sound methodology, no major conceptual mistakes (10)

### 2. Originality & Insight (20 pts)
- Thoughtful extensions or ablations beyond pure reproduction (10)
- Quality of analysis and interpretation of results (10)

### 3. Implementation & Reproducibility (20 pts)
- Clean, well-organized GitHub repo with documentation (10)
- Can reproduce main results with provided scripts (10)

### 4. Written Reports (20 pts)
- Midterm report completeness and clarity (5)
- Final report structure, clarity, and depth (10)
- Correct and adequate citation of prior work (5)

### 5. Presentation & Teamwork (10 pts)
- Clear, well-timed presentation; all members contribute (5)
- Clear description of individual responsibilities and balanced workload (5)

> Bonus up to +5 pts for publishable-level results (e.g., near state-of-the-art on subset, strong novel analysis, or submission-ready draft)
---

## Policy on GenAI Use

To ensure authentic learning and fair assessment: 

### Allowed GenAI use (with disclosure): 
• Brainstorming ideas and clarifying concepts (e.g., “Explain cross-entropy loss”). 
• Assistance with debugging after you attempt to fix it. 
• Help with English phrasing (grammar, minor style edits). 

### Not allowed: 
• Generating code that you then claim as your own without understanding it. 
• Generating large portions of the report (sections, literature review) via GenAI. 
• Generating experimental results or “fake” figures/tables. 
• Asking GenAI to directly implement the assigned paper or project end-to-end. 

### Neutralization mechanisms: 
1.  Oral Defense & Q&A: 
- In certain cases, each team member will be asked detailed technical questions (e.g., why you chose a learning rate, implications of certain layers). 
- Inability to explain code or design choices will significantly reduce credit for that part, regardless of how good the code looks. 

2.  Code Review: 
- Instructors may ask you to walk through key functions line-by-line. 
- Random code snippets may be chosen for explanation. 

3.  Reproducibility Checks: 
- The instructor may run your code in a clean environment. 
- If scripts break or hyperparameters are undocumented, points are deducted. 

4.  Process Documentation: 
- You must maintain a brief development log (in LOG.md) describing weekly progress, key decisions, and issues encountered. 
- Logs must be consistent with Git commit history. 

5.  GenAI Use Disclosure: 
- Add a short section in both midterm and final reports titled “Use of GenAI Tools” describing where/how you used them (if at all). 
- Honest disclosure will not be penalized; hidden use discovered later will be. 

6.  Writing Style Consistency: 
- Report writing style will be compared with previous coursework when available. Abrupt, unexplained shifts may trigger closer review and questioning. 

> By combining technical questioning, code walkthroughs, and reproducibility checks, reliance on GenAI for core intellectual work will yield little advantage. Understanding and original thought are what will be graded. 


## quick reference: where to find content

| section | file |
|---------|------|
| problem statement | `01-problem.md` |
| project goals | `02-goal.md` |
| related work / papers | `03-related-work.md` |
| research notes | `04-research-notes.md` |
| dataset details | `05-dataset.md` |
| solution approach | `06-solution.md` |
| constraints | `07-constraints.md` |
| model architecture | `08-architecture.md` |
| tech stack | `09-stack.md` |
| repo structure | `10-structure.md` |
| workflow | `11-workflow.md` |
| timeline | `12-timeline.md` |
| references | `13-references.md` |