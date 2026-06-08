# final report quickstart

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


## quick reference: where to find content

| report section | our file |
|---------------|----------|
| title + abstract | `01-title-and-abstract.md` |
| introduction | `02-introduction.md`, `01-project-definition/01-problem.md`, `01-project-definition/02-goal.md` |
| related work | `03-related-work.md` |
| data + preprocessing | `04-data-and-preprocessing.md`, `01-project-definition/05-dataset.md` |
| methodology | `05-methodology.md`, `01-project-definition/06-solution.md`, `01-project-definition/08-architecture.md` |
| experiments + results | `06-experiments-and-results.md` |
| discussion | `07-discussion.md` |
| conclusion | `08-conclusion.md` |
| team contributions | `09-team-contributions.md` |
| references | `10-references.md` |
| appendix | `11-appendix.md` |
| final report | `12-final-report.md` |