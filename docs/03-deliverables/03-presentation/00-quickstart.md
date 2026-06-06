# presentation quickstart

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


## quick reference: where to find content

| slide section | our file |
|---------------|----------|
| motivation + problem | `01-motivation-and-problem.md`, `01-project-definition/01-problem.md`, `01-project-definition/02-goal.md` |
| data + method | `02-data-and-method.md`, `01-project-definition/05-dataset.md`, `01-project-definition/06-solution.md`, `01-project-definition/08-architecture.md` |
| results + analysis | `03-results-and-analysis.md`, `02-results/03-performance-comparison.md`, `02-results/04-results-analysis.md` |
| limitations + future work | `04-limitations-and-future-work.md` |
| presentation | `05-presentation.md` |