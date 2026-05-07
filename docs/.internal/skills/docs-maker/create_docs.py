#!/usr/bin/env python3
import os
import sys


def build_structure():
    return {
        ".internal": [
            ("00-quickstart.md", "10-min overview of the research"),
            ("speckit", "similar projects & comparisons (landscape first)"),
            ("02-references.md", "academic references & papers"),
            ("03-research-notes.md", "exploration & learnings"),
        ],
        "research": [
            ("00-quickstart.md", "10-min overview of the research"),
            ("01-related-work.md", "similar projects & comparisons (landscape first)"),
            ("02-references.md", "academic references & papers"),
            ("03-research-notes.md", "exploration & learnings"),
        ],
        "project-definition": [
            ("00-quickstart.md", "10-min project overview"),
            ("01-problem.md", "problem statement & context"),
            ("02-goal.md", "project goals & objectives"),
            ("03-solution.md", "proposed solution approach"),
            ("04-dataset.md", "data sources & specifications"),
            ("05-constraints.md", "should do / should not do"),
            ("06-stack.md", "technology stack & dependencies"),
            ("07-architecture.md", "system design & data flow"),
            ("08-workflow.md", "development workflow & process"),
            ("09-structure.md", "project directory structure"),
        ],
        "planning": [
            ("00-quickstart.md", "10-min overview of planning docs"),
            ("01-proposal.md", "business/project proposal"),
            ("02-timeline.md", "milestones & schedules"),
        ],
        "api": [
            ("00-quickstart.md", "10-min api overview"),
            ("01-api-design.md", "api specifications & contracts"),
        ],
        "results": [
            ("00-quickstart.md", "10-min overview of results"),
            ("01-evaluation.md", "model/solution evaluation metrics"),
            ("02-testing.md", "testing methodology & results"),
            ("03-performance-comparison.md", "benchmarks vs. baselines"),
            ("04-results-analysis.md", "detailed findings & insights"),
            ("05-future-work.md", "next steps & open problems"),
        ],
        "presentation": [
            ("00-quickstart.md", "10-min overview of presentation materials"),
            ("01-presentation-script.md", "slide scripts & talking points"),
        ],
    }


def ensure_docs(project_root):
    docs_root = os.path.join(project_root, "docs")
    structure = build_structure()
    created = []
    skipped = []
    # sections to never create or modify (treat as read-only)
    IGNORE_SECTION_NAMES = {"skills"}
    for section, files in structure.items():
        # if the section name indicates an ignored area, skip it entirely
        if section.split(os.sep)[-1] in IGNORE_SECTION_NAMES:
            for filename, desc in files:
                relpath = os.path.join("docs", section, filename).replace(os.sep, "/")
                skipped.append(relpath)
            continue

        section_dir = os.path.join(docs_root, section)
        os.makedirs(section_dir, exist_ok=True)
        for filename, desc in files:
            path = os.path.join(section_dir, filename)
            relpath = os.path.relpath(path, project_root).replace(os.sep, "/")
            name_no_ext = os.path.splitext(filename)[0]
            first_line = f"{relpath} - {name_no_ext}: {desc}\n"
            if os.path.exists(path):
                skipped.append(relpath)
                continue
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(first_line + "\n")
                fh.write(f"# {name_no_ext}\n\n")
                fh.write(desc + "\n")
            created.append(relpath)
    return created, skipped


def main(argv):
    project_root = os.path.abspath(argv[1]) if len(argv) > 1 else os.getcwd()
    created, skipped = ensure_docs(project_root)
    for p in created:
        print(f"+ {p}")
    for p in skipped:
        print(f"~ {p}")
    print(f"\nSummary: +{len(created)} created, ~{len(skipped)} skipped")


if __name__ == "__main__":
    main(sys.argv)
