# speckit workflow

## claude chat as project manager
### phase 1
I want to create a [project-name] that will [project-descriptions]. We are going to use Spec Kit for the implementation. If you don't know Spec Kit, search for it [look it up]. We need to have phases, and each phase will be done with a spec using Spec Kit.

### phase 2
0K, we need a markdown file (use canvas) with the excutive summary and the phases following that so that I can add it in the project folder.

## claude code (ops 4.6) as 
### phase 3
/speckit.constitution this is project that will be implemented following the plan in the `docs/.internal/speckit/02-specs.md` file. the implementation should follow best practices for implementing a project.

### phase 4
/speckit.specify read `docs/.internal/speckit/02-specs.md` and create a spec for the first phase.

## speckit workflow for each spec using claude code (ops 4.6)

for each of the 9 specs above, you'll run:
1. `/speckit.constitution` - define or amend project principles (`.specify/memory/constitution.md`)
2. `/speckit.specify` - describe the what/why (i'll write these prompts for you)
3. `/speckit.clarify` - resolve ambiguities
4. `/speckit.plan` - generate planظ
5. `/speckit.checklist` - generate validation checklists
6. `/speckit.tasks` - create the tasks file so that a cheaper llm model can implement without problems then back to claude code (ops 4.6) to review the implementation 
7. `/speckit.analyze` - check consistency (pre-implementation)

## speckit workflow for each spec using open code (glm 5)

8. `/speckit.implement` - after claude code ops 4.6 wrote this spec so now u can implement phase 1 of this spec @specs/spec-name/tasks.md

great let's move to phase 2 of this spec @specs/spec-name/tasks.md

## speckit workflow after implement spec: back to claude code (ops 4.6)

9. `/speckit.review` - review the implementation of this spec @specs/spec-name/

## speckit workflow after review spec: back to open code (glm 5)

10. `/speckit-fix` - fix the implementation of this review @specs/spec-name/review/001-review.md

## speckit workflow after review fix spec: back to claude code (ops 4.6)

11. `/speckit.review` - review again to generate 002-review.md and confirms the fixes are clean and no new issues were introduced by the fixes from previous review @@specs/spec-name/review/001-review.md and