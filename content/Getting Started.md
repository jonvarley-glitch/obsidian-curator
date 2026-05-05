# Getting Started

A practical guide to using this Obsidian vault day-to-day. For naming rules, frontmatter conventions, and maintenance cadence, see [[Conventions]].

## First-Run Setup

Most plugins ship with sensible defaults. Two need a quick manual configuration the first time you open the vault:

### Periodic Notes

Settings -> Community plugins -> Periodic Notes:

- **Daily Notes**: format `YYYY-MM-DD`, folder `Daily`, template `Templates/daily.md`.
- **Weekly Notes**: format `gggg-[W]ww`, folder `Daily`, template `Templates/weekly-review.md`.
- Disable monthly / quarterly / yearly unless you actively use them.

### QuickAdd

Settings -> Community plugins -> QuickAdd. Add a "Capture" action for the meeting template:

- Name: "New Meeting"
- Capture format: from `Templates/meeting.md`
- File name format: `{{DATE:YYYY-MM-DD}} - {{VALUE:Customer}} - {{VALUE:Topic}}`
- Folder: `03-Meetings/`

Repeat for any other templates you create from often (customer hub, project, system).

### Tasks

The Tasks plugin works out of the box. Default emoji syntax (`📅 due`, `⏫ priority`, `✅ done`) is what the queries on Home, daily notes, and the weekly review expect.

### Excalidraw

The plugin ships pre-configured to save drawings into `Assets/Excalidraw/`. No further setup needed -- see the [Diagrams](#diagrams-with-excalidraw) section below.

## Quick Reference

| I want to...                        | Do this                                                                 |
| ----------------------------------- | ----------------------------------------------------------------------- |
| Capture a quick thought             | `Ctrl/Cmd + N` — lands in `00-Inbox`                                   |
| Create a meeting note               | QuickAdd or Templater → Meeting template                                |
| Start a daily note                  | Click today's date in the Calendar sidebar                              |
| Find a customer's info              | `Ctrl/Cmd + O` → type the customer name                                |
| Search across all notes             | `Ctrl/Cmd + Shift + F` for full-text search                            |
| Ask the AI a question about a topic | Open Copilot chat → ask naturally (e.g. "summarise the Acme Corp account") |
| See my task board                   | Open [[Task Board]] in `13-Tasks/`                                      |
| Browse all customers / meetings / projects / systems | Open the matching `.base` view in `Bases/` |
| Triage everything in the Inbox      | Run the `/triage-inbox` slash command in Cursor or Claude Code          |
| Polish the current meeting note     | Run `/polish-meeting`                                                   |
| Generate a weekly review            | Run `/weekly-summary`                                                   |
| Document a system from raw notes    | Run `/document-system`                                                  |
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

7. **Quick pass (2 minutes)** — fill in Key Takeaways, convert commitments into `- [ ]` checkboxes with a Tasks-format due date (`📅 YYYY-MM-DD`), and add `[[Customer]]` or `[[Person]]` wikilinks for anyone mentioned.
8. **AI polish** — ask Cursor or Obsidian Copilot to clean up the note. For example: *"Polish my meeting note from the Acme Corp architecture review today."* The AI will fix grammar, restructure messy bullet dumps into headed sections, standardise formatting, and ensure the note is optimised for search and RAG retrieval. This is especially valuable for long or complex meetings where your raw notes are rough.

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
| Learning something new about a product | `04-Knowledge/` with Knowledge template | You know the type and product area |
| Half-formed thought during a walk | `00-Inbox/` | Capture first, classify later |

The Inbox is a safety net, not a workflow step. Most of your notes should bypass it entirely.

## Creating Notes by Type

### Meeting Notes

The most common note type. Use the meeting template.

**Naming**: `YYYY-MM-DD - Customer - Topic.md`
Examples:
- `2026-03-09 - Acme Corp - Architecture Review.md`
- `2026-03-10 - SA Bi-Weekly - Team Update.md`
- `2026-03-11 - Internal - Onboarding Debrief.md`

**Where**: `03-Meetings/`

**Frontmatter** (auto-filled by template):

```yaml
---
type: meeting
date: 2026-03-09
customer: "[[Acme Corp]]"
status: active
---
```

**Tips**:
- Always set the `customer` field — this is how the customer hub page finds related meetings via Dataview.
- For internal meetings (no customer), set `customer` to `"Internal"` or omit it.
- Use `[[Person Name]]` wikilinks for attendees and people mentioned in the discussion.
- Convert action items into `- [ ]` checkboxes — the Tasks plugin shows them on the Home dashboard, daily note, and weekly review.

### Customer Notes

Only create a new customer hub page when you're assigned a new account.

**Naming**: `Customer Name.md` (Title Case)
**Where**: `01-Customers/`

Use the customer template. It automatically creates Dataview queries that pull in all meetings, projects, and tasks linked to that customer.

### Knowledge Notes

For anything you learn that isn't tied to a specific meeting or project: product deep-dives, architecture patterns, sizing guidance, platform features.

**Naming**: Descriptive Title Case. Prefix with a customer name only if the knowledge is customer-specific.
Examples:
- `Migration Playbook.md`
- `Acme Corp - Network Architecture.md`

**Where**: `04-Knowledge/`

**Tips**:
- Set `product-area` in frontmatter to a value from your own taxonomy.
- These are the highest-value notes for RAG queries — invest time in making them clear and well-structured.

### Project Notes

For tracking a specific engagement, PoC, or deliverable.

**Naming**: `Customer - Project Name.md`
**Where**: `02-Projects/`

### System Notes

For documenting a specific technology, product, or integration (a CRM, a data warehouse, an identity provider).

**Naming**: `Vendor Product.md` Title Case. Examples: `Salesforce Sales Cloud.md`, `Snowflake.md`, `Okta.md`.

**Where**: `04-Knowledge/`

Use the system template. It includes an Excalidraw architecture embed and structured sections for data flows, integrations, APIs, and owners. Set the `customer` field if the system is customer-specific; leave it blank for generic / internal systems.

### Everything Else

| Type          | Folder             | When to use                                    |
| ------------- | ------------------ | ---------------------------------------------- |
| Competition   | `06-Competition/`  | Competitor analysis, displacement strategies    |
| Demo          | `07-Demos/`        | Demo scripts, runbooks, talk tracks            |
| Workshop      | `09-Workshops/`    | Workshop materials and session notes            |
| Certification | `10-Certifications/` | Study notes, exam prep, training materials    |
| Partner       | `11-Partners/`     | Partner profiles, GTM strategies               |
| Internal      | `12-Internal/`     | Onboarding, sales process, internal tooling guides |
| Industry      | `05-Industry/`     | Sector-specific research (e.g. Financial Services) |

## Linking Best Practices

Links are the backbone of the vault. They build the knowledge graph that makes search, backlinks, and AI retrieval powerful.

### When to Link

- **Always** link customer names: `[[Acme Corp]]`, `[[Globex]]`, `[[Initech]]`
- **Always** link people when you reference them: `[[Sarah Chen]]`
- **Always** link related projects and meetings: `see [[Acme Corp - Architecture Review]]`
- **Sometimes** link knowledge notes when referencing a concept: `using [[Migration Playbook|the playbook]]`

### When Not to Link

- Don't link product or technology names that don't have their own notes
- Don't link generic terms (meeting, project, task)
- Don't over-link within the same note — once per section is enough

### Link Syntax

```markdown
[[Acme Corp]]                              # basic wikilink
[[Acme Corp|Acme]]                         # display alias
[[2026-03-09 - Acme Corp - Review]]        # link to a specific meeting
```

## Using AI in the Vault

### Copilot (Conversational AI)

Open the Copilot panel from the right sidebar. You can ask it questions about your vault:

- "Summarise the Acme Corp account — key contacts, current projects, and recent meetings"
- "What do we know about Globex's monitoring setup?"
- "Draft a follow-up email for the Initech meeting on March 9th"
- "What are the main competitive differences between Vendor A and Vendor B?"
- "Help me prepare for a discovery meeting with a new financial services customer"

Copilot uses your vault content as context (RAG), so the better your notes are structured, the better the answers.

### Smart Connections

This plugin builds a vector index of your vault. It surfaces semantically related notes in the sidebar — useful for discovering connections you might not have linked manually.

### Tips for AI-Friendly Notes

- **Frontmatter matters**: `type`, `customer`, `product-area`, and `status` fields are used by Dataview queries and help the AI understand context.
- **Clear headings**: H2/H3 structure helps the AI chunk content for retrieval.
- **Wikilinks**: They create explicit relationships the AI can follow.
- **One note, one purpose**: A focused note retrieves better than a dump of unrelated content.

## Diagrams with Excalidraw

Excalidraw is the primary diagramming tool. It ships pre-configured to save drawings into `Assets/Excalidraw/`.

### Creating a drawing

1. Command Palette (`Ctrl/Cmd + P`) -> "Excalidraw: Create new drawing".
2. Name it `<Note Title> - <Diagram Topic>` (for example `Acme Corp - High-Level Architecture`).
3. Sketch.

### Embedding a drawing

```markdown
![[Acme Corp - High-Level Architecture.excalidraw]]
```

The `system`, `project`, and `customer` templates already include this embed pattern in their Architecture sections. Create the matching drawing once via the Command Palette and the embed renders automatically thereafter.

### Excalidraw vs Mermaid

| Use Excalidraw for | Use Mermaid for |
| ------------------ | --------------- |
| Architecture diagrams (C4 context / container / component) | A 5-line sequence diagram inside a meeting note |
| Whiteboard-style sketches in workshops | A simple state machine you can express in 4 lines |
| Anything you'll want to redraw freely later | Anything where opening a canvas is overkill |

Mermaid blocks are fenced as ```` ```mermaid ```` -- supported natively by Obsidian.

## Bases Views

In addition to Dataview tables on hub pages, the vault ships interactive `.base` views in the `Bases/` folder:

| Base | Use it to... |
| ---- | ------------ |
| `Customers.base` | Browse, sort, and filter all customers (Active, By Tier views included). |
| `Meetings.base` | Scan recent meetings (Last 30 Days view), or group by customer. |
| `Projects.base` | See active projects, group by customer. |
| `Systems.base` | Inventory of `system` notes; filter by category, vendor, customer. |

Add or rename views inline -- changes save back to the `.base` file. Bases queries run noticeably faster than Dataview on large vaults, so reach for these when you want to scan or filter, and keep Dataview for the embedded tables on hub pages.

## Managing Tasks

Tasks in this vault follow a simple principle: **tasks live where the work lives**. An action item from a meeting stays in that meeting note. A project milestone stays in that project note. The **Tasks plugin** then aggregates them onto your Home page, daily note, and any custom view so nothing falls through the cracks.

### Task Syntax

A basic task:

```markdown
- [ ] Send architecture proposal to Acme Corp
```

A task with a **due date** (use Tasks-plugin emoji syntax, or the date-picker shortcut `Ctrl/Cmd + P` -> "Tasks: Create or edit task"):

```markdown
- [ ] Send architecture proposal to Acme Corp 📅 2026-03-14
```

A task with a **scheduled date** and **priority**:

```markdown
- [ ] Prepare sizing estimate 📅 2026-03-20 ⏫
```

You can keep a customer wikilink in the task text — Tasks treats it as plain text and Obsidian still resolves the link:

```markdown
- [ ] Sizing estimate for [[Globex]] 📅 2026-03-20
```

A **completed** task (click the checkbox; Tasks records the completion date automatically):

```markdown
- [x] Send follow-up email to [[Initech]] 📅 2026-03-10 ✅ 2026-03-10
```

> Inline Dataview fields like `[due:: 2026-03-14]` still work for custom Dataview queries, but the Tasks emoji format is what the queries on Home, daily, and weekly notes expect.

### Where to Create Tasks

| Situation                            | Create the task in                     |
| ------------------------------------ | -------------------------------------- |
| Action item from a meeting           | The meeting note's **Action Items** section |
| Follow-up to send after a meeting    | The meeting note's **Follow-ups** section   |
| Project milestone or deliverable     | The project note's **Tasks** section        |
| Personal to-do for the day           | Your daily note's **Tasks** section         |
| Standalone task not tied to a note   | [[Task Board]] (Kanban) or your daily note  |

The key insight: you don't need to duplicate tasks or move them around. The Tasks plugin pulls them from wherever they are.

### The Task Board (Kanban)

Open [[Task Board]] in `13-Tasks/` for a visual drag-and-drop board with columns:

- **Inbox** — new tasks that need triaging
- **This Week** — committed work for the current week
- **In Progress** — actively working on
- **Waiting On** — blocked on someone else
- **Done** — completed (archive periodically)

The Kanban board is best for tasks that aren't tied to a specific meeting or project, or for getting a visual overview of your week.

### How Tasks Appear on Your Dashboards

**Home page** — Open Tasks (sorted by due date), Overdue, and Due This Week sections, all powered by the Tasks plugin.

**Daily note** — Due Today and Overdue sections.

**Customer hub pages** — each customer's Open Tasks section shows incomplete tasks from notes linked to that customer.

**Weekly review** — shows tasks completed in the past 7 days plus anything carried over.

### Task Workflow

**After a meeting:**
1. Review the notes you took
2. Convert commitments into `- [ ]` checkboxes in the Action Items section
3. Use `Ctrl/Cmd + P` -> "Tasks: Create or edit task" to add a due date / priority via the picker
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

- **Don't over-engineer it.** The `- [ ]` checkbox is the only tool you need. Due dates, priorities, and customer links are optional but helpful for filtering.
- **Use the Tasks picker.** `Ctrl/Cmd + P` -> "Tasks: Create or edit task" beats typing emojis manually.
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
4. After the meeting, spend 2 minutes: fill in Key Takeaways, add `- [ ]` action items with a `📅 YYYY-MM-DD` due date, add `[[Customer]]` wikilinks
5. Ask Cursor or Copilot (or run `/polish-meeting`) to polish the note — fixes language, adds structure, optimises for search
6. The meeting automatically appears on the customer hub page (Dataview) and Home dashboard (Tasks plugin)

### New Customer Onboarding

1. Create a customer hub page from the Customer template
2. Fill in Overview, Key Contacts, and industry
3. Start creating meeting notes linked to the customer
4. As projects emerge, create project notes linked to the customer
5. CRM data can go in `90-Archive/` with a link from the customer's Reference Data section

### Building a Knowledge Base

1. After a training session, meeting, or learning something new — create a knowledge note
2. Structure it with clear headings and set the `product-area`
3. Link it from relevant customer or project notes
4. These notes become the foundation for AI-powered Q&A about your domain
