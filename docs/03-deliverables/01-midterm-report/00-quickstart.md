# midterm report quickstart

ieee conference format (two-column), 5-8 pages.
template: https://www.ieee.org/conferences/publishing/templates.html

this guide maps each section to what graders expect and what content from our project docs to use. tick every bullet before submitting.

---

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
| introduction | `02-introduction.md`, `01-problem.md` |
| related work | `03-related-work.md` |
| methodology | `04-methodology.md`, `05-dataset.md`, `06-solution.md`, `08-architecture.md` |
| preliminary results | `05-preliminary-experiments-and-results.md` |
| planned work | `06-planned-work-and-timeline.md`, `11-workflow.md` |
| team contributions | `07-team-contributions.md` |
| references | `08-references.md` |
| midterm report | `09-midterm-report.md` |