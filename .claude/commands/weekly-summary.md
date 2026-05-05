---
description: Generate a weekly review covering the past 7 days
---

# Weekly Summary

Generate a weekly review note for the past 7 days. Create or update the matching `weekly-review` note in `Daily/` using the [[Templates/weekly-review]] template (`Daily/` ships with the vault and is where Periodic Notes places weekly notes by default).

Pull from these sources:

1. **Meetings** — every note in `03-Meetings/` whose `date` is within the last 7 days. Summarise key decisions and outcomes per customer.
2. **Completed tasks** — use the Tasks plugin "done after 7 days ago" filter. Aggregate by customer / project.
3. **Open commitments carried over** — overdue tasks from the same scope.
4. **Active customers / projects** — anything in `01-Customers/` or `02-Projects/` updated this week (from file mtime if available, otherwise inferred from linked meetings).
5. **Decisions captured** — scan project notes for `### YYYY-MM-DD - Decision Title` H3 headings dated this week.

Produce these sections in the weekly review note:

- **Highlights** — 3-5 bullets, the things that mattered most.
- **Customer Activity** — table grouped by customer.
- **Decisions Made** — bullet list with date and link to source note.
- **Open Tasks Carried Over** — actionable list, with due dates.
- **Lessons / Reflections** — leave blank for the user to fill in.

Cite source notes with `[[wikilinks]]`. Do not fabricate. If a section has no content, write "_None this week._" rather than inventing entries.
