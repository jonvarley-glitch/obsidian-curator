---
description: Clean up the current meeting note (structure, tasks, links) without losing content
---

# Polish Meeting

Polish the current meeting note. The note may be a raw transcript, sticky-note dump, or rough outline.

Apply the following passes, in order:

1. **Frontmatter** — ensure `type: meeting`, `customer: "[[...]]"`, `date: YYYY-MM-DD`, `attendees: []` are populated where the content supports it.
2. **Structure** — ensure H2 sections in this order: `## Attendees`, `## Agenda`, `## Discussion`, `## Decisions`, `## Action Items`, `## Follow-ups`. Move existing content under the right heading.
3. **Action items** — extract every commitment ("X will do Y") into the **Action Items** section as a `- [ ]` checkbox. If a date is mentioned, append `📅 YYYY-MM-DD` (Tasks plugin format). If no owner is named, leave the action under the meeting host.
4. **Wikilinks** — wrap every customer, person, project, and system name in `[[...]]` once per section.
5. **Prose** — rewrite fragmentary bullets into full sentences. Keep the original meaning; do not infer or fabricate.
6. **Diagrams** — preserve any `![[*.excalidraw]]` embeds and Mermaid blocks verbatim.

Output: the polished note in place. Summarise the changes you made (sections added, tasks extracted, links added).
