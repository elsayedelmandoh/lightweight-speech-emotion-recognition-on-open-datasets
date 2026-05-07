# feature-writer

Generate comprehensive feature documentation from spec + implementation.

## Description

Creates a detailed markdown file in `docs/features/` that explains a feature's purpose, architecture, usage, and team guidance.

**Input:** Feature spec folder (e.g., `specs/001-shared-infrastructure/`)
**Output:** `docs/features/{feature-name}.md`

## Usage

```bash
/feature-writer <feature-name>
```

Example:
```bash
/feature-writer shared-infrastructure
/feature-writer watchlist-monitor-agent
```

## What Gets Generated

The skill extracts from `specs/{feature}/` and `src/` to create a markdown document with:

1. **Overview** - Feature purpose, why built it, strategic importance
2. **Quick Start** - 5-minute setup for developers
3. **Architecture** - Design decisions, key components, data flow
4. **API Reference** - Main classes/functions with signatures
5. **Configuration** - Settings, environment variables, tuning
6. **Examples** - Practical usage patterns
7. **Testing** - Test structure, how to run, expected results
8. **Troubleshooting** - Common issues and solutions
9. **Team Guide** - How to explain to stakeholders, key metrics
10. **Next Steps** - Related features, known limitations

## Implementation Notes

- Reads `spec.md` for requirements and context
- Reads `plan.md` for architecture
- Scans implementation files to extract actual signatures
- Generates markdown using SpecKit conventions
- Creates `docs/features/` if it doesn't exist

## Example Output Structure

```
docs/features/
├── watchlist-monitor-agent.md
├── shared-infrastructure.md
└── index.md (auto-generated links)
```

## Global Skill

This is a reusable skill available globally at `~/.agents/skills/feature-writer/SKILL.md`

---

**Created:** 2026-04-01 | **Renamed:** 2026-04-01
**Related:** `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`
