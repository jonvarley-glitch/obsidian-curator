# Vault Manifest for AI Agents

This file describes the structure and conventions of this Obsidian vault so that AI agents (Cursor, Claude Code, or any MCP-connected tool) can read and modify notes correctly.

## Vault Purpose

Knowledge base for a Solution Architect at Elastic, managing customers, meetings, projects, competitive intelligence, demos, workshops, and certifications.

## Folder Structure

| Folder | Purpose | Files |
| ------ | ------- | ----- |
| `00-Inbox/` | Quick capture, unsorted notes. Process weekly. | 0 |
| `01-Customers/` | One hub page per customer. Person notes also live here. | 14 |
| `02-Projects/` | Time-bound project work, linked to customers. | 7 |
| `03-Meetings/` | One note per meeting, linked to customer and project. | 27 |
| `04-Knowledge/` | Elastic platform knowledge base articles. | 22 |
| `05-Industry/` | Vertical-specific content (FSI, healthcare, etc.). | 0 |
| `06-Competition/` | Competitor analysis and positioning notes. | 1 |
| `07-Demos/` | Demo scripts and custom demo runbooks. | 1 |
| `08-ESATs/` | Elastic Solution Architecture Templates -- value-and-outcome statements for large opportunities. | 5 |
| `09-Workshops/` | Workshop outlines and materials. | 2 |
| `10-Certifications/` | Training and certification tracking. | 8 |
| `11-Partners/` | Partner GTM strategy, contacts, and joint customer notes. | 1 |
| `12-Internal/` | Elastic internal processes, APEX training, SFDC, onboarding. | 23 |
| `13-Tasks/` | Task Board (Kanban) for visual task tracking. | 1 |
| `90-Archive/` | Archived CRM exports, completed, or inactive items. | 67 |
| `Templates/` | Templater templates. Do not edit directly -- managed by vault-forge. | 14 |
| `Prompts/` | AI prompt templates for Copilot plugin. | 4 |
| `Assets/` | Images, PDFs, and other attachments. | 0 |

## Root Files

| File | Purpose |
| ---- | ------- |
| `Home.md` | Dashboard with Dataview queries: active customers, recent meetings, open tasks, overdue items, ESATs, certifications. |
| `Getting Started.md` | Usage guide: daily workflow, note creation by type, inbox vs. direct filing, task management, linking best practices, AI usage, keyboard shortcuts. |
| `Conventions.md` | Naming, tagging, frontmatter, and maintenance rules. |
| `CLAUDE.md` | This file -- AI agent manifest. |

## Note Types

Every note has a `type` frontmatter field. Valid types: `customer`, `person`, `meeting`, `project`, `knowledge`, `industry`, `competition`, `demo`, `esat`, `partner`, `workshop`, `certification`, `daily`, `weekly-review`.

## Frontmatter Conventions

- Relationship fields use wikilinks: `customer: "[[Acme Corp]]"`
- Dates use ISO 8601: `date: 2026-03-09`
- Status values: `active`, `inactive`, `completed`, `archived`, `draft`
- No blank properties -- omit fields that don't apply
- `product-area` where applicable: `Search`, `Observability`, `Security`, `Platform`

## File Naming

- Evergreen notes: Title Case with spaces (`Acme Corp.md`)
- Dated notes: `YYYY-MM-DD - Title.md` (e.g. `2026-03-09 - Nomura - Architecture Review.md`)
- No special characters: `# | ^ : % [[ ]]`

## Tags

Cross-cutting themes only: `#security`, `#observability`, `#search`, `#migration`, `#performance`. Never duplicate frontmatter fields.

## Task Syntax

Tasks are inline `- [ ]` checkboxes that live where the work lives (meeting notes, project notes, daily notes). Dataview aggregates them onto the Home page and daily notes.

```markdown
- [ ] Send proposal to customer [due:: 2026-03-14]
- [ ] Prepare sizing estimate [due:: 2026-03-20] [customer:: [[M&G]]]
```

The `Task Board.md` in `13-Tasks/` is a Kanban board for visual task management.

## When Creating or Modifying Notes

1. Always include `type` and `status` in frontmatter
2. Use wikilinks for customer, project, and people references
3. If the note type is known, file directly into the correct folder (not Inbox)
4. Place unclassified quick captures in `00-Inbox/`
5. One note per discrete unit (one meeting, one topic)
6. Start note body with `# Title` matching the filename, then H2 sections
7. Scope Dataview queries to specific folders with `LIMIT`
8. For meeting notes: always set `customer` field so the customer hub page picks it up

## When Polishing Notes

1. Keep all original information intact -- never fabricate or infer content
2. Fix typos, grammar, incomplete sentences; rewrite fragments into clear prose
3. Ensure proper H2/H3 hierarchy; break long bullet dumps into headed sections
4. Use `[[Customer]]` wikilinks for customer names in body text
5. Elastic product names (Kibana, Elasticsearch, APM) stay as plain text -- not wikilinks
6. Standardise bullet style (`-`), bold usage, table format
7. Add `product-area` to frontmatter where content clearly relates to Search, Observability, or Security
8. Remove filler/boilerplate but preserve all technical detail
