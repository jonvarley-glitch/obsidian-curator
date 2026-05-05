# Vault Manifest for AI Agents

This file describes the structure and conventions of this Obsidian vault so that AI agents (Cursor, Claude Code, or any MCP-connected tool) can read and modify notes correctly.

## Vault Purpose

Knowledge base for a Solution Architect, managing customers, meetings, projects, competitive intelligence, demos, workshops, partners, and certifications.

## Folder Structure

| Folder | Purpose |
| ------ | ------- |
| `00-Inbox/` | Quick capture, unsorted notes. Process weekly. |
| `01-Customers/` | One hub page per customer. Person notes also live here. |
| `02-Projects/` | Time-bound project work, linked to customers. |
| `03-Meetings/` | One note per meeting, linked to customer and project. |
| `04-Knowledge/` | Platform / product knowledge base articles. |
| `05-Industry/` | Vertical-specific content (financial services, healthcare, etc.). |
| `06-Competition/` | Competitor analysis and positioning notes. |
| `07-Demos/` | Demo scripts and custom demo runbooks. |
| `09-Workshops/` | Workshop outlines and materials. |
| `10-Certifications/` | Training and certification tracking. |
| `11-Partners/` | Partner GTM strategy, contacts, and joint customer notes. |
| `12-Internal/` | Internal processes, training, sales tooling, onboarding. |
| `13-Tasks/` | Task Board (Kanban) for visual task tracking. |
| `90-Archive/` | Archived CRM exports, completed, or inactive items. |
| `Templates/` | Templater templates. Do not edit directly -- managed by vault-forge. |
| `Prompts/` | AI prompt templates for Copilot plugin. |
| `Bases/` | Standalone Bases views (`.base` files) for Customers, Meetings, Projects, Systems. |
| `Daily/` | Daily notes and weekly reviews (Periodic Notes target). |
| `Assets/` | Images, PDFs, and other attachments. |
| `Assets/Excalidraw/` | Excalidraw drawings (`.excalidraw.md`). Embedded via `![[wikilink]]`. |

## Root Files

| File | Purpose |
| ---- | ------- |
| `Home.md` | Dashboard. Dataview blocks for active customers / recent meetings / active projects / active systems / certifications; Tasks-plugin blocks for open tasks / overdue / due this week. Browse line links to the Task Board and the Bases views. |
| `Getting Started.md` | Usage guide: daily workflow, note creation by type, inbox vs. direct filing, task management, linking best practices, AI usage, keyboard shortcuts. |
| `Conventions.md` | Naming, tagging, frontmatter, and maintenance rules. |
| `CLAUDE.md` | This file -- AI agent manifest. |

## Note Types

Every note has a `type` frontmatter field. Valid types: `customer`, `person`, `meeting`, `project`, `knowledge`, `system`, `industry`, `competition`, `demo`, `partner`, `workshop`, `certification`, `daily`, `weekly-review`.

The `system` type documents a specific technology, product, or integration (e.g. a CRM, data warehouse, identity provider). System notes live in `04-Knowledge/` and are filtered by `type = "system"`.

## Frontmatter Conventions

- Relationship fields use wikilinks: `customer: "[[Acme Corp]]"`
- Dates use ISO 8601: `date: 2026-03-09`
- Status values: `active`, `inactive`, `completed`, `archived`, `draft`
- No blank properties -- omit fields that don't apply
- `product-area` is freeform -- define your own taxonomy and apply it consistently

## File Naming

- Evergreen notes: Title Case with spaces (`Acme Corp.md`)
- Dated notes: `YYYY-MM-DD - Title.md` (e.g. `2026-03-09 - Acme Corp - Architecture Review.md`)
- No special characters: `# | ^ : % [[ ]]`

## Tags

Cross-cutting themes only. Never duplicate frontmatter fields. Flat namespace (no nesting).

## Diagrams

**Excalidraw is the default diagramming tool.** Drawings live in `Assets/Excalidraw/` and embed into notes with a wikilink:

```markdown
![[Acme Corp - High-Level Architecture.excalidraw]]
```

Use Excalidraw for: architecture diagrams, C4 context/container/component, sequence flows you want to redraw freely, whiteboard sessions, workshop captures.

**Use Mermaid only for trivial inline diagrams** where round-tripping to Excalidraw is overkill — for example a five-line sequence diagram inside a meeting or project note. Fenced as ```` ```mermaid ```` blocks.

When polishing a note, never fabricate diagram content. Preserve `![[*.excalidraw]]` embeds and existing Mermaid blocks verbatim.

## Bases vs Dataview

Both work in this vault.

- **Dataview** powers the inline tables on hub pages (`Home.md`, customer notes, project notes). Use Dataview when the table is a section of a larger note.
- **Bases** (Obsidian core plugin) powers standalone interactive views. The `.base` files in `Bases/` are filterable, sortable, and faster on large vaults. Add a new Base when you want a dedicated view that lives outside any single note.

## Decisions Log

Significant architecture and project decisions live as `### YYYY-MM-DD - Decision Title` H3 sections inside the relevant project note (under the **Decisions Log** heading shipped by `templates/project.md`). Capture each decision with four bullets:

- **Context:** what triggered the decision
- **Options considered:** alternatives weighed
- **Decision:** what was chosen
- **Consequences:** trade-offs and follow-ups

This keeps decisions searchable (`### YYYY-` matches across the vault) without a dedicated `adr` note type. The `decision-matrix` Copilot prompt drafts these.

## Task Syntax

Tasks are inline `- [ ]` checkboxes that live where the work lives (meeting notes, project notes, daily notes). The **Tasks plugin** aggregates them onto the Home page, daily notes, and weekly review.

```markdown
- [ ] Send proposal to customer 📅 2026-03-14
- [ ] Prepare sizing estimate for [[Acme Corp]] 📅 2026-03-20 ⏫
```

Tasks emoji syntax: `📅` due date, `⏳` scheduled, `🛫` start, `✅` completed, `⏫` high priority, `🔼` medium, `🔽` low.

The `Task Board.md` in `13-Tasks/` is a Kanban board for visual task management.

## When Creating or Modifying Notes

1. Always include `type` and `status` in frontmatter
2. Use wikilinks for customer, project, and people references
3. If the note type is known, file directly into the correct folder (not Inbox)
4. Place unclassified quick captures in `00-Inbox/`
5. One note per discrete unit (one meeting, one topic)
6. Start note body with `# Title` matching the filename, then H2 sections
7. Scope Dataview queries to specific folders with `FROM` and add `LIMIT`
8. Tasks-plugin queries (```` ```tasks ```` blocks) should set `hide backlink` and a sensible `limit N`
9. For meeting notes: always set `customer` field so the customer hub page picks it up

## When Polishing Notes

1. Keep all original information intact -- never fabricate or infer content
2. Fix typos, grammar, incomplete sentences; rewrite fragments into clear prose
3. Ensure proper H2/H3 hierarchy; break long bullet dumps into headed sections
4. Use `[[Customer]]` wikilinks for customer names in body text
5. Standardise bullet style (`-`), bold usage, table format
6. Add `product-area` to frontmatter where content clearly maps to one
7. Remove filler/boilerplate but preserve all technical detail
8. Preserve diagrams verbatim: `![[*.excalidraw]]` embeds and ```` ```mermaid ```` fenced blocks must not be edited or removed
