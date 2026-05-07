---
name: readme-writer
description: >
  Write a professional README.md for the current project by scanning all key
  project folders and files (docs/, src/, data/, notebooks/, models/, outputs/).
  Use this skill whenever the user says "write my README", "generate README.md",
  "create a README for my project", "write the readme", or anything implying they
  want a project README generated or regenerated. Also trigger if the user says
  "my project is done, write the docs front page" or "make the root README".
  Always overwrites the existing README.md with a freshly generated version.
---

# README Writer

Generate a professional `README.md` at the project root by synthesizing content
from the project's existing files — docs, notebooks, source code, config files,
and any existing README.

---

## How to Run

```bash
python {SKILL_DIR}/scripts/create_readme.py {PROJECT_ROOT}
```

Replace `{SKILL_DIR}` with the absolute path to this skill folder, and
`{PROJECT_ROOT}` with the absolute path to the user's project root.

The script will scan the project, synthesize content, and write `README.md` to
the project root. It prints a summary of what it found and used.

---

## What the Script Reads

The script does a full context harvest before writing. In priority order:

| Source | What it extracts |
|--------|-----------------|
| `docs/project-definition/01-problem.md` | Problem statement for Overview hook |
| `docs/project-definition/02-goal.md` | Success criteria and goals |
| `docs/project-definition/03-solution.md` | Approach and key design decisions → Key Features |
| `docs/project-definition/06-stack.md` | Tech stack |
| `docs/planning/01-proposal.md` | Fallback for any missing section |
| `docs/results/*.md` | Results, metrics, evaluation outcomes |
| `docs/results/*.png`, `*.jpg` | Result images shown in header gallery |
| `requirements.txt` / `environment.yml` | Dependencies for Setup section |
| `app.py` / `main.py` / `run.py` | Entry point for Usage section |
| `.readme-config.json` (project root) | Author info, badges, social links |
| `README.md` (existing) | Fallback — mine for any context not found elsewhere |

Anything not found is replaced with a clearly marked `<!-- TODO -->` placeholder.

---

## Badge and Author Config

The script looks for `.readme-config.json` in the project root. If present, it
uses the values to populate badges and the author section. If absent, it
generates placeholders the user can fill in.

```json
{
  "github_repo": "username/repo-name",
  "huggingface_space": "username/space-name",
  "twitter_handle": "handle",
  "linkedin_profile": "profile-slug",
  "linkedin_post_url": "https://...",
  "author_name": "Your Name",
  "author_title": "NLP Engineer",
  "linktree": "https://linktr.ee/handle",
  "conda_env_name": "myenv",
  "python_version": "3.12",
  "entry_point": "app.py"
}
```

All fields are optional. The script skips badges for missing fields rather than
breaking.

---

## Output Structure

The script produces a `README.md` with this exact section order:

```
# {Project Title}

{Badges row}

{Image gallery — if result images found}

## Table of Contents

## Overview

## Key Features

## Setup
  ### 0. Prerequisites
  ### 1. Clone the Repository
  ### 2. Create Conda Environment
  ### 3. Environment Variables

## Usage

## Contributing

## Author
```

### Section Rules

**Title**: Use the project directory name, title-cased. If
`docs/project-definition/` exists with content, extract the project name from
there if it appears.

**Badges**: Always include GitHub badge if `github_repo` is set. Include
HuggingFace badge only if `huggingface_space` is set (not all projects deploy to
HF). Include Twitter, LinkedIn profile, and LinkedIn post badges only if the
respective config fields are set.

Badge format (copy exactly, substituting values):
```markdown
[![GitHub](https://img.shields.io/badge/GitHub-{repo_slug}-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{github_repo})
[![Hugging Face](https://img.shields.io/badge/Space-Hugging%20Face-yellow?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/spaces/{huggingface_space})
[![X](https://img.shields.io/badge/X-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/{twitter_handle})
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/{linkedin_profile}/)
[![LinkedIn Post](https://img.shields.io/badge/LinkedIn%20Post-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)]({linkedin_post_url})
```

`{repo_slug}` = the repo name part with underscores replacing hyphens (for
display), e.g. `sentiment__sleuth`.

**Image gallery**: If `docs/results/` contains image files (`.png`, `.jpg`,
`.gif`), include the first two as a side-by-side gallery using this pattern:

```markdown
<p align="center">
  <img src="docs/results/{img1}" alt="{project_name} — pos results" width="45%">
  &nbsp; &nbsp;
  <img src="docs/results/{img2}" alt="{project_name} — neg results" width="45%">
</p>
```

If only one image, center it at 60% width. If none, omit the gallery entirely.

**Overview**: Three tight paragraphs, no bullets:
1. Hook — what painful problem this solves and who feels it (1-2 sentences,
   pulled from the problem statement)
2. Solution and technical aha moment — what you built and why it works
   (1-2 sentences)
3. Results — one concrete metric or outcome that proves it worked

Keep this factual and direct. No marketing fluff. No "In today's world..." openers.

**Key Features**: 3-5 bullet points, each `**Bold Label:** description.` Pull
labels from the solution's key design decisions or the most important
capabilities. Be specific — avoid vague labels like "Scalable" or "Fast".

**Setup**: Fill in conda env name and python version from config if set,
otherwise use `myenv` and `3.12`. Fill in entry point from config or auto-detect
(check for `app.py`, `main.py`, `run.py` in that order).

If the project has a `.env.example` file, list those variable names in the
Environment Variables step. Otherwise show one generic placeholder line.

**Usage**: Show the command to run the main entry point. If `app.py` exists and
uses Gradio or Streamlit, add the note about opening the local URL.

**Author**: Use `author_name`, `author_title`, and `linktree` from config if
set. Defaults: `Elsayed Elmandoh`, `NLP Engineer`, `https://linktr.ee/elsayedelmandoh`.
Format:
```markdown
## Author

{name} - {title}

* Connect on LinkedIn and X [Linktree]({linktree})
```

---

## Quality Rules

- All prose in Overview and Key Features must be written in **active voice**.
- No em dashes (`—`) anywhere in the output.
- No placeholder text left unexplained: any field the script cannot fill must be
  marked `<!-- TODO: fill in X -->` so the user knows exactly what to complete.
- Do not make up metrics or features not supported by the source files.
- Keep the Setup section accurate: only list prerequisites actually needed by
  the project.
