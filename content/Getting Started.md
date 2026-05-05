# Getting Started

A practical guide to using this Obsidian vault day-to-day. For naming rules, frontmatter conventions, and maintenance cadence, see [[Conventions]].

## Quick Reference

| I want to...                        | Do this                                                                 |
| ----------------------------------- | ----------------------------------------------------------------------- |
| Capture a quick thought             | `Ctrl/Cmd + N` — lands in `00-Inbox`                                   |
| Create a meeting note               | QuickAdd or Templater → Meeting template                                |
| Start a daily note                  | Click today's date in the Calendar sidebar                              |
| Find a customer's info              | `Ctrl/Cmd + O` → type the customer name                                |
| Search across all notes             | `Ctrl/Cmd + Shift + F` for full-text search                            |
| Ask the AI a question about a topic | Open Copilot chat → ask naturally (e.g. "summarise the Nomura account") |
| See my task board                   | Open [[Task Board]] in `13-Tasks/`                                      |
| See what's unlinked or orphaned     | Command palette → "Find orphaned files"                                 |

## Daily Workflow

### Morning

1. **Open your daily note** — click today's date in the Calendar panel (left sidebar). This creates a new note from the Daily template with sections for Focus, Meetings, Notes, and Tasks.
2. **Review Home** — open [[Home]] to see active customers, recent meetings, open tasks, and upcoming certification deadlines at a glance.
3. **Plan your day** — fill in the Focus and Meetings sections of your daily note.

### During the Day

4. **Before a meeting** — create a meeting note using the Meeting template. Pre-fill the agenda. Link it to the customer with `[[Customer Name]]`. The note goes straight into `03-Meetings/` — not the Inbox.
5. **During the meeting** — take notes in the Discussion section. Don't worry about formatting; capture everything. Use `- [ ]` for action items as they come up.
6. **Quick captures** — if something doesn't fit a template, press `Ctrl/Cmd + N` to create a note in `00-Inbox`. You'll file it later.

### After a Meeting — Polish

7. **Quick pass (2 minutes)** — fill in Key Takeaways, convert commitments into `- [ ]` checkboxes with `[due:: YYYY-MM-DD]`, and add `[[Customer]]` or `[[Person]]` wikilinks for anyone mentioned.
8. **AI polish** — ask Cursor or Obsidian Copilot to clean up the note. For example: *"Polish my meeting note from the Elastic OpEx Forum today."* The AI will fix grammar, restructure messy bullet dumps into headed sections, standardise formatting, and ensure the note is optimised for search and RAG retrieval. This is especially valuable for long or complex meetings where your raw notes are rough.

### End of Day

9. **Tidy the inbox** — review anything in `00-Inbox`. Either move it to the right folder or link it from a relevant note and leave it there.
10. **Fill in action items** — make sure every `- [ ]` task has context (which customer, what's due).
11. **Write the End of Day Review** in your daily note.

### Weekly

10. **Weekly review** — use the Weekly Review template to reflect on what happened, what's coming next, and whether any projects need status updates.

## Inbox vs. Direct Filing

Not everything goes through the Inbox. The rule is simple: **if you know what it is, file it directly. If you don't, use the Inbox.**

| Situation | Where it goes | Why |
| --------- | ------------- | --- |
| Meeting starting in 5 minutes | `03-Meetings/` with Meeting template | You know the date, type, and customer |
| New customer assigned to you | `01-Customers/` with Customer template | You know it's a customer hub page |
| Interesting idea from a Slack thread | `00-Inbox/` | Unstructured — needs thinking about where it belongs |
| URL someone shared that you want to read later | `00-Inbox/` | Not sure if it's knowledge, competition, or just noise |
| Learning something new about Elasticsearch | `04-Knowledge/` with Knowledge template | You know the type and product area |
| Half-formed thought during a walk | `00-Inbox/` | Capture first, classify later |

The Inbox is a safety net, not a workflow step. Most of your notes should bypass it entirely.

## Creating Notes by Type

### Meeting Notes

The most common note type. Use the meeting template.

**Naming**: `YYYY-MM-DD - Customer - Topic.md`
Examples:
- `2026-03-09 - Nomura - Architecture Review.md`
- `2026-03-10 - SA Bi-Weekly - AutoOps Update.md`
- `2026-03-11 - Internal - APEX Training Debrief.md`

**Where**: `03-Meetings/`

**Frontmatter** (auto-filled by template):

```yaml
---
type: meeting
date: 2026-03-09
customer: "[[Nomura]]"
status: active
---
```

**Tips**:
- Always set the `customer` field — this is how the customer hub page finds related meetings via Dataview.
- For internal meetings (no customer), set `customer` to `"Elastic"` or omit it.
- Use `[[Person Name]]` wikilinks for attendees and people mentioned in the discussion.
- Convert action items into `- [ ]` checkboxes — they'll show up on the Home dashboard.

### Customer Notes

Only create a new customer hub page when you're assigned a new account.

**Naming**: `Customer Name.md` (Title Case)
**Where**: `01-Customers/`

Use the customer template. It automatically creates Dataview queries that pull in all meetings, projects, and tasks linked to that customer.

### Knowledge Notes

For anything you learn that isn't tied to a specific meeting or project: product deep-dives, architecture patterns, sizing guidance, platform features.

**Naming**: Descriptive Title Case. Prefix with a customer name only if the knowledge is customer-specific.
Examples:
- `LogsDB Migration Guide.md`
- `Nomura - Firewall Architecture.md`

**Where**: `04-Knowledge/`

**Tips**:
- Set `product-area` in frontmatter to `Search`, `Observability`, `Security`, or `Platform`.
- These are the highest-value notes for RAG queries — invest time in making them clear and well-structured.

### Project Notes

For tracking a specific engagement, PoC, or deliverable.

**Naming**: `Customer - Project Name.md`
**Where**: `02-Projects/`

### ESATs

For documenting large opportunities. ESATs capture customer context, solution architecture, sizing, value, and risks.

**Naming**: `Customer - ESAT Description.md`
**Where**: `08-ESATs/`

### Everything Else

| Type          | Folder             | When to use                                    |
| ------------- | ------------------ | ---------------------------------------------- |
| Competition   | `06-Competition/`  | Competitor analysis, displacement strategies    |
| Demo          | `07-Demos/`        | Demo scripts, runbooks, talk tracks            |
| Workshop      | `09-Workshops/`    | Workshop materials and session notes            |
| Certification | `10-Certifications/` | Study notes, exam prep, training materials    |
| Partner       | `11-Partners/`     | Partner profiles, GTM strategies               |
| Internal      | `12-Internal/`     | Onboarding, sales process, APEX, SFDC guides   |
| Industry      | `05-Industry/`     | Sector-specific research (e.g. Financial Services) |

## Linking Best Practices

Links are the backbone of the vault. They build the knowledge graph that makes search, backlinks, and AI retrieval powerful.

### When to Link

- **Always** link customer names: `[[Nomura]]`, `[[M&G]]`, `[[Barclays]]`
- **Always** link people when you reference them: `[[Sarah Chen]]`
- **Always** link related projects and meetings: `see [[Nomura - Architecture Review]]`
- **Sometimes** link knowledge notes when referencing a concept: `using [[LogsDB Migration Guide|LogsDB]]`

### When Not to Link

- Don't link Elastic product names (Kibana, Elasticsearch, APM) — they're not notes
- Don't link generic terms (meeting, project, task)
- Don't over-link within the same note — once per section is enough

### Link Syntax

```markdown
[[Nomura]]                              # basic wikilink
[[Nomura|Nomura Holdings]]              # display alias
[[2026-03-09 - Nomura - Review]]        # link to a specific meeting
```

## Using AI in the Vault

### Copilot (Conversational AI)

Open the Copilot panel from the right sidebar. You can ask it questions about your vault:

- "Summarise the Nomura account — key contacts, current projects, and recent meetings"
- "What do we know about M&G's observability setup?"
- "Draft a follow-up email for the Barclays meeting on March 9th"
- "What are the main competitive differences between Elastic and OpenSearch?"
- "Help me prepare for a discovery meeting with a new financial services customer"

Copilot uses your vault content as context (RAG), so the better your notes are structured, the better the answers.

### Smart Connections

This plugin builds a vector index of your vault. It surfaces semantically related notes in the sidebar — useful for discovering connections you might not have linked manually.

### Tips for AI-Friendly Notes

- **Frontmatter matters**: `type`, `customer`, `product-area`, and `status` fields are used by Dataview queries and help the AI understand context.
- **Clear headings**: H2/H3 structure helps the AI chunk content for retrieval.
- **Wikilinks**: They create explicit relationships the AI can follow.
- **One note, one purpose**: A focused note retrieves better than a dump of unrelated content.

## Managing Tasks

Tasks in this vault follow a simple principle: **tasks live where the work lives**. An action item from a meeting stays in that meeting note. A project milestone stays in that project note. Dataview then aggregates them all onto your Home page and daily note so nothing falls through the cracks.

### Task Syntax

A basic task:

```markdown
- [ ] Send architecture proposal to Nomura
```

A task with a **due date** (Dataview can sort and filter on this):

```markdown
- [ ] Send architecture proposal to Nomura [due:: 2026-03-14]
```

A task linked to a **customer** (useful when the task isn't inside a customer-linked note):

```markdown
- [ ] Prepare sizing estimate [due:: 2026-03-20] [customer:: [[M&G]]]
```

A **completed** task (click the checkbox or type `x`):

```markdown
- [x] Send follow-up email to Barclays [due:: 2026-03-10]
```

### Where to Create Tasks

| Situation                            | Create the task in                     |
| ------------------------------------ | -------------------------------------- |
| Action item from a meeting           | The meeting note's **Action Items** section |
| Follow-up to send after a meeting    | The meeting note's **Follow-ups** section   |
| Project milestone or deliverable     | The project note's **Tasks** section        |
| Personal to-do for the day           | Your daily note's **Tasks** section         |
| Standalone task not tied to a note   | [[Task Board]] (Kanban) or your daily note  |

The key insight: you don't need to duplicate tasks or move them around. Dataview pulls them from wherever they are.

### The Task Board (Kanban)

Open [[Task Board]] in `13-Tasks/` for a visual drag-and-drop board with columns:

- **Inbox** — new tasks that need triaging
- **This Week** — committed work for the current week
- **In Progress** — actively working on
- **Waiting On** — blocked on someone else
- **Done** — completed (archive periodically)

The Kanban board is best for tasks that aren't tied to a specific meeting or project, or for getting a visual overview of your week.

### How Tasks Appear on Your Dashboards

**Home page** — the Open Tasks section shows all incomplete `- [ ]` checkboxes from every note in the vault, sorted by due date. The Overdue section highlights anything past its due date.

**Daily note** — shows tasks due today and anything overdue, automatically pulled from across the vault.

**Customer hub pages** — each customer's Open Tasks section shows incomplete tasks from notes linked to that customer.

**Weekly review** — shows tasks completed in the past 7 days, so you can see what you accomplished.

### Task Workflow

**After a meeting:**
1. Review the notes you took
2. Convert commitments into `- [ ]` checkboxes in the Action Items section
3. Add `[due:: YYYY-MM-DD]` to anything with a deadline
4. These immediately appear on your Home page and daily note

**Start of day:**
1. Open your daily note — check the "Due Today" and "Overdue" sections
2. Add any ad-hoc tasks for the day in the Tasks section
3. Optionally open the [[Task Board]] for a visual overview

**End of week:**
1. Run a weekly review — the template automatically shows what you completed
2. Move stale Kanban cards or re-date overdue tasks
3. Plan next week's priorities

### Tips

- **Don't over-engineer it.** The `- [ ]` checkbox is the only tool you need. Due dates and customer links are optional but helpful for filtering.
- **Keep tasks close to context.** A task in a meeting note has all the context right there — who said what, what was discussed. A task ripped out into a separate system loses that.
- **Use the Kanban board for the big picture.** It's great for weekly planning and triaging, not for every small to-do.
- **Check off tasks where they live.** When you complete something, go to the original note and tick the checkbox. It updates everywhere automatically.

## Keyboard Shortcuts

| Shortcut                  | Action                          |
| ------------------------- | ------------------------------- |
| `Ctrl/Cmd + N`            | New note (lands in Inbox)       |
| `Ctrl/Cmd + O`            | Quick switcher (find any note)  |
| `Ctrl/Cmd + Shift + F`    | Search across all notes         |
| `Ctrl/Cmd + P`            | Command palette                 |
| `Ctrl/Cmd + E`            | Toggle edit/preview mode        |
| `Ctrl/Cmd + Click`        | Open link in new tab            |
| `[[`                      | Start typing a wikilink         |
| `Alt + Enter` (Templater) | Insert template into current note |

## Archiving Notes

When a customer becomes inactive or a project completes:

1. Update the `status` field in frontmatter to `archived` or `completed`
2. Move the file to `90-Archive/`
3. Wikilinks from other notes will continue to work — Obsidian tracks moves automatically

## Common Patterns

### Meeting Follow-up Flow

1. Create meeting note from template before the meeting — goes straight to `03-Meetings/`
2. Pre-fill the agenda and customer link
3. Take raw notes during the meeting — don't worry about formatting
4. After the meeting, spend 2 minutes: fill in Key Takeaways, add `- [ ]` action items with `[due:: YYYY-MM-DD]`, add `[[Customer]]` wikilinks
5. Ask Cursor or Copilot to polish the note — fixes language, adds structure, optimises for search
6. The meeting automatically appears on the customer hub page and Home dashboard via Dataview

### New Customer Onboarding

1. Create a customer hub page from the Customer template
2. Fill in Overview, Key Contacts, and industry
3. Start creating meeting notes linked to the customer
4. As projects emerge, create project notes and ESATs linked to the customer
5. CRM data can go in `90-Archive/` with a link from the customer's Reference Data section

### Building a Knowledge Base

1. After a training session, meeting, or learning something new — create a knowledge note
2. Structure it with clear headings and set the `product-area`
3. Link it from relevant customer or project notes
4. These notes become the foundation for AI-powered Q&A about Elastic capabilities
