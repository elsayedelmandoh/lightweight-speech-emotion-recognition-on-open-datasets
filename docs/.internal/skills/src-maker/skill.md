# Agent Skill: Create Project Skeleton

Purpose
-------
This skill automates creating a minimal Python project skeleton in the workspace. It is workspace-scoped and intended for quick project bootstrapping.

Scope / Outcome
----------------
- Create the following files and folders (one run of the skill):
  - `src/` (package folder)
  - `notebooks/` (folder for notebooks)
  - `.env` (example runtime env — may include secrets placeholders)
  - `.env.example` (safe, committed example env)
  - `.gitignore`
  - `app.py` (minimal runnable entrypoint)
  - `README.md` (project description + quickstart)
  - `requirements.txt` (dependency list)

Inputs
------
- Project name (optional)
- Python version (optional)
- Any required packages to seed `requirements.txt` (optional)

Step-by-step workflow
---------------------
1. Validate inputs (use defaults when missing).
2. Create directories: `src/` and `notebooks/`.
3. Create `__init___.py` inside `src/` if desired (keeps package import-friendly).
4. Write `.gitignore` with common Python ignores.
5. Write `.env.example` with placeholder variables; write `.env` as a copy only when explicitly requested.
6. Create `app.py` with a minimal runnable example (Flask or plain script depending on inputs).
7. Create `README.md` with a short project description and commands to run.
8. Create `requirements.txt` based on the requested packages (or leave empty comment).
9. Run basic validation: ensure files created and `python -m pip check` is not required at this stage.

Decision points and branching
----------------------------
- If user requests a web app: scaffold `app.py` as a small Flask app and include `Flask` in `requirements.txt`.
- If the user prefers a CLI: create `app.py` with a `__main__` entry and sample `argparse` usage.
- For `.env`: never write real secrets into repository; default to writing only `.env.example` and prompt before creating `.env`.

Quality criteria / completion checks
----------------------------------
- All listed files and folders exist in the workspace.
- `app.py` runs with `python app.py` producing a short success message (or starts Flask on a port when scaffolded).
- `README.md` contains a Quickstart section with commands to create a virtual environment and install `requirements.txt`.
- `.env.example` contains only placeholder values.

Iteration and clarifying questions
---------------------------------
If inputs are missing or ambiguous, ask:
- "Do you want a Flask web app or a simple CLI script?"
- "Which packages (if any) should be prepopulated in `requirements.txt`?"
- "Create `.env` now or only `.env.example`?"

Examples: prompts to run this skill
----------------------------------
- "Create a Python project skeleton with Flask and add Flask to requirements."
- "Bootstrap a project named `sqlinjection-xss-detection` with `src/` and `notebooks/`."
- "Create only `README.md`, `.gitignore`, and `requirements.txt` for a library project."

Suggested follow-ups / related customizations
-------------------------------------------
- Add automated tests: scaffold `tests/` and a `pytest` setup.
- Add a `pyproject.toml` or `setup.cfg` for packaging.
- Add pre-commit hooks and a `Makefile` for common tasks.

How to run (operator notes)
---------------------------
- This skill is intended to be executed by an agent or developer tooling that can create files in the workspace. It should never insert real secrets into files.

Revision notes
--------------
- Drafted to seed new projects quickly; update templates (app.py, README) to match project conventions.
