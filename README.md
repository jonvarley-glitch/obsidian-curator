# Vault Forge

[![CI](../../actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)

Automated setup tool for an Obsidian vault tailored for a Solution Architect. Creates the full vault structure -- folders, templates, AI prompts, plugin installs, plugin configs, starter Bases views, and Obsidian configuration -- from a single `config.yaml`.

## Quick Start

```bash
pip install -r requirements.txt
python setup_vault.py
```

This creates the vault at the path specified in `config.yaml` (default: `~/Documents/ObsidianVaults/SAVault`). Open Obsidian, choose "Open folder as vault", and point it at that directory.

## CLI Options

```bash
python setup_vault.py --validate          # parse config, print summary, write nothing
python setup_vault.py --skip-plugins      # offline / CI; skip plugin downloads
python setup_vault.py --vault-path PATH   # override vault.path from config
python setup_vault.py --config PATH       # use a different config.yaml
```

## What Gets Created

**20 folders** with numbered prefixes for visual ordering:

```
SAVault/
├── 00-Inbox/            Quick capture
├── 01-Customers/        Customer hub pages
├── 02-Projects/         Time-bound project work
├── 03-Meetings/         Meeting notes
├── 04-Knowledge/        Platform / product / system knowledge base
├── 05-Industry/         Vertical content (FSI, healthcare, etc.)
├── 06-Competition/      Competitor analysis
├── 07-Demos/            Demo scripts and runbooks
├── 09-Workshops/        Workshop materials
├── 10-Certifications/   Training and cert tracking
├── 11-Partners/         Partner profiles and GTM
├── 12-Internal/         Company-internal notes
├── 13-Tasks/            Kanban Task Board
├── 90-Archive/          Completed and archived items
├── Templates/           Templater templates
├── Prompts/             AI prompt templates
├── Bases/               Bases views (Customers, Meetings, Projects, Systems)
├── Daily/               Daily notes and weekly reviews (Periodic Notes)
├── Assets/              Attachments
└── Assets/Excalidraw/   Excalidraw drawings
```

**14 Templater templates** for consistent note creation: customer, person, meeting, project, knowledge, **system**, industry, competition, demo, partner, workshop, certification, daily, weekly-review.

**8 AI prompt templates** for Copilot: account summary, meeting follow-up, competitive positioning, weekly review, **decision matrix**, **system documentation**, **discovery questions**, **architecture review**.

**15 community plugins** auto-installed: Copilot, Smart Connections, Templater, QuickAdd, Dataview, **Tasks**, Kanban, Calendar, Periodic Notes, Obsidian Git, Homepage, Tag Wrangler, Linter, Find Orphaned Files, **Excalidraw**.

**Plugin configurations** (data.json) shipped for Templater, Homepage, Linter, and Excalidraw so they work out of the box.

**4 starter Bases views** for `Customers`, `Meetings`, `Projects`, `Systems` -- standalone interactive tables that complement the Dataview queries on hub pages.

**Obsidian configuration**: app settings, core plugin enable/disable (including the `bases` core plugin), community plugin list, and `.gitignore`.

**Starter content**: Home.md dashboard, CLAUDE.md AI agent manifest, Conventions.md naming guide, Getting Started.md usage guide, and a 5-lane Kanban Task Board.

## Configuration

Edit `config.yaml` to customise:

- `vault.path` -- where the vault is created
- `folders` -- the folder structure
- `plugins` -- which community plugins to install
- `core_plugins` -- which core plugins to enable/disable
- `app_settings` -- Obsidian editor settings (merged into `.obsidian/app.json` on each run; config wins on conflicts)
- `note_types` -- valid `type:` frontmatter values; `--validate` checks every template against this list

Re-run `python setup_vault.py` after changes. It's safe to re-run:

- Existing user notes are never overwritten.
- Customised `.base` files are preserved.
- Per-plugin `data.json` files are preserved.
- Top-level `.obsidian/*.json` files (community-plugins, core-plugins, hotkeys, appearance) are preserved if they already exist; only `.obsidian/app.json` is rewritten so `app_settings:` edits propagate.
- `Templates/*.md` and `Prompts/*.md` **are refreshed each run** -- they are project-owned artifacts so users get bug fixes and new templates. If you want to customise a template, save it under a different filename (e.g. `my-meeting.md`) so re-runs leave it alone.
- `.gitignore` is regenerated each run.

## Bringing Existing Notes In

The recommended workflow is to drop new content into the vault's `00-Inbox/` and let an AI agent triage it.

1. Drop `.md` files (or anything you want imported) into `00-Inbox/`.
2. Open the vault folder in Cursor (or any AI agent that can read the vault).
3. Run the project-level slash command `/triage-inbox`, or ask in chat:

   > "Tidy up the notes in my Inbox -- add frontmatter, rename them, and move them into the right folder."

The vault's `CLAUDE.md` describes the folder layout, frontmatter conventions, and note types, so any decent agent can classify and file correctly.

For richer content (e.g. `.docx`, `.pptx`), convert to Markdown first using a tool like Pandoc, then drop the resulting Markdown into the Inbox.

## Diagrams

**Excalidraw is the primary diagramming tool.** Drawings live in `Assets/Excalidraw/` and embed into any note via wikilink:

```markdown
![[Acme Corp - High-Level Architecture.excalidraw]]
```

Use Excalidraw for: architecture diagrams, C4 context/container/component, sequence flows you want to redraw freely, whiteboard sessions, workshop captures.

**Mermaid** stays available for trivial inline diagrams (a five-line sequence diagram inside a meeting note, for example), fenced as ```` ```mermaid ```` blocks.

The `system` template, the `project` template, and the `customer` template all ship with an Excalidraw embed placeholder for the architecture section -- create the matching drawing once via Command Palette -> "Excalidraw: Create new drawing" and the embed renders automatically.

## Bases

[Bases](https://help.obsidian.md/bases) is a 2026 core Obsidian plugin that turns YAML frontmatter into fast, sortable, filterable database views. Vault Forge ships starter `.base` files in `Bases/`:

| Base | What it shows |
| ---- | ------------- |
| `Customers.base` | All customers, with industry / tier / status. Sub-views for Active, By Tier. |
| `Meetings.base` | All meetings, with date / customer / project. Sub-views for Last 30 Days, By Customer. |
| `Projects.base` | All projects, with customer / status / dates. Sub-views for Active, By Customer. |
| `Systems.base` | All `system` notes, with vendor / category / owner. Sub-views for Active, By Category, By Customer. |

**When to use Bases vs Dataview?**

- Use **Dataview** when you want an inline table inside a hub page (Home, customer note, project note).
- Use **Bases** when you want a standalone interactive view that lives in `Bases/` and can be reordered, filtered, and grouped on the fly.

Both ship enabled. Pick whichever fits the situation.

## AI Stack

The vault is designed for three layers of AI:

| Layer | Tool | Use Case |
| ----- | ---- | -------- |
| In-vault chat | **Obsidian Copilot** | Ask questions about your notes, generate content |
| Passive discovery | **Smart Connections** | Auto-surface related notes as you write |
| Power operations | **Cursor / Claude Code** | Bulk processing, triaging the inbox, polishing meetings |

Configure API keys in the Copilot and Smart Connections plugin settings after opening the vault in Obsidian.

The project ships four `.claude/commands/` slash commands that work in both Cursor and Claude Code:

- `/triage-inbox` -- classify, frontmatter, rename, and file every note in `00-Inbox/`.
- `/polish-meeting` -- structure the current meeting note, extract tasks, add wikilinks.
- `/weekly-summary` -- generate a weekly review from meetings, completed tasks, and decisions.
- `/document-system` -- create or update a `system` note from the current note's content.

## Recipes

Three short worked examples that exercise the vault end-to-end.

### Logging a discovery meeting

1. Open `00-Inbox/`. Use Templater to insert the **meeting** template into a new note.
2. Capture notes during the meeting, with action items as `- [ ]` lines.
3. After the meeting, run `/polish-meeting` to structure headings, extract tasks (with `📅` due dates), and link customer / people.
4. Action items now appear automatically on Home, daily, and the customer's hub page via the Tasks plugin.

### Documenting a new system

1. From a discussion note in any folder, run `/document-system`.
2. The agent creates `04-Knowledge/<Vendor Product>.md` from the `system` template, populates `vendor` / `category` / `owner` / `status`, and fills the body sections from the source.
3. Open the new note. Click the `![[<Title> - Architecture.excalidraw]]` embed -> "Create" to draw the architecture.
4. The system instantly appears in `Bases/Systems.base` and on any customer hub page that links to it via the customer's Dataview block.

### Weekly review

1. Use Periodic Notes' "Open this week's review" command, or insert the `weekly-review` template manually.
2. Run `/weekly-summary` to fill the note from meetings, completed Tasks, and `### YYYY-MM-DD - Decision Title` H3 sections in project notes from the past 7 days.
3. Add the **Lessons / Reflections** content yourself.

## Project Structure

```
vault-forge/
├── .cursor/rules/       Cursor AI rules for this project
├── .claude/commands/    Project-level slash commands (Cursor + Claude Code)
├── .github/workflows/   CI (ruff + yaml + pytest)
├── setup_vault.py       Vault scaffolding script
├── config.yaml          All configuration
├── requirements.txt     Runtime Python dependencies
├── requirements-dev.txt ruff + pytest
├── templates/           Obsidian template source files
├── prompts/             AI prompt template source files
├── obsidian_config/     .obsidian JSON configs (top-level + per-plugin data.json)
├── content/             Starter vault content (Home, CLAUDE, Conventions, Getting Started, Task Board)
│   └── bases/           Starter Bases views (.base files)
└── tests/               pytest suite
```

## Development

```bash
pip install -r requirements-dev.txt
ruff check .
pytest -q
python setup_vault.py --validate
```

CI runs the same three steps on every push / PR.
