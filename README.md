# Vault Forge

Automated setup tool for an Obsidian vault tailored for a Solution Architect at Elastic. Creates the full vault structure including folders, templates, AI prompts, plugin installations, and Obsidian configuration -- all from a single `config.yaml`.

## Quick Start

```bash
# Install dependencies (includes pandoc via pypandoc_binary)
pip install -r requirements.txt

# Run vault setup
python setup_vault.py
```

This creates the vault at the path specified in `config.yaml` (default: `~/Documents/ObsidianVaults/ElasticSA`). Open Obsidian, choose "Open folder as vault", and point it to that directory.

## What Gets Created

**18 folders** with numbered prefixes for visual ordering:

```
ElasticSA/
├── 00-Inbox/          Quick capture
├── 01-Customers/      Customer hub pages
├── 02-Projects/       Time-bound project work
├── 03-Meetings/       Meeting notes
├── 04-Knowledge/      Elastic platform knowledge base
├── 05-Industry/       Vertical content (FSI, etc.)
├── 06-Competition/    Competitor analysis
├── 07-Demos/          Demo scripts and runbooks
├── 08-ESATs/          Elastic Solution Architecture Templates
├── 09-Workshops/      Workshop materials
├── 10-Certifications/ Training and cert tracking
├── 11-Partners/       Partner profiles and GTM
├── 12-Internal/       Elastic internal notes
├── 13-Tasks/          Kanban boards and task tracking
├── 90-Archive/        Completed and archived items
├── Templates/         Templater templates
├── Prompts/           AI prompt templates
└── Assets/            Attachments
```

**14 Templater templates** for consistent note creation: customer, person, meeting, project, knowledge, industry, competition, demo, esat, partner, workshop, certification, daily, weekly-review.

**4 AI prompt templates** for Copilot: account summary, meeting follow-up, competitive positioning, weekly review.

**13 community plugins** auto-installed: Copilot, Smart Connections, Templater, QuickAdd, Dataview, Kanban, Calendar, Periodic Notes, Obsidian Git, Homepage, Tag Wrangler, Linter, Find Orphaned Files.

**Obsidian configuration**: app settings, core plugin enable/disable, community plugin list, and `.gitignore`.

**Starter content**: Home.md dashboard with Dataview queries, CLAUDE.md AI agent manifest, Conventions.md naming guide, Getting Started.md usage guide.

## Configuration

Edit `config.yaml` to customise:

- `vault.path` -- where the vault is created
- `folders` -- the folder structure
- `plugins` -- which community plugins to install
- `core_plugins` -- which core plugins to enable/disable
- `app_settings` -- Obsidian editor settings
- `note_types` -- valid type values for frontmatter
- `status_values` -- valid status values

Re-run `python setup_vault.py` after changes. It's safe to re-run -- existing user notes are never overwritten.

## Import Existing Notes

Import `.docx`, `.pptx`, `.md`, and `.txt` files into the vault. The script auto-detects two directory layouts:

**Customer-first** (recommended for Google Drive exports):

```
Customers/
├── Nomura/               # Customer name → frontmatter customer
│   ├── Account Plan.pptx
│   ├── Meetings/         # Subdirectory → type hint (meeting)
│   │   └── weekly-sync.docx
│   ├── Opportunities/    # → type hint (project)
│   │   └── proposal.pptx
│   └── Archived/         # → status: archived
│       └── old-doc.docx
└── M&G/
    └── Discovery Sheet.docx
```

**Type-first** (pre-sorted by note type):

```
my-notes/
├── meeting/acme/sync.docx    # type=meeting, customer=acme
├── certification/cert.docx   # type=certification
└── loose-file.txt            # type from filename patterns or AI
```

```bash
# Preview what would be imported (always do this first)
python import_notes.py ~/Downloads/Customers --dry-run

# Import for real
python import_notes.py ~/Downloads/Customers
```

### Reclassify with Cursor

After import, ask Cursor to review and improve the classifications:

> "Read the notes I just imported and reclassify anything that looks wrong -- fix types, titles, and add metadata like product-area and industry."

Cursor reads the actual content of each note and can move files, rename them, update frontmatter, and enrich metadata -- all using its built-in Claude access. No separate API key or subscription needed.

### Day-to-day: meeting transcripts

For ongoing use, drop meeting transcripts (Gemini notes, `.docx` exports, etc.) into the vault's `00-Inbox` folder, then ask Cursor:

> "Tidy up the notes in my Inbox -- add frontmatter, rename them, and move to the right folder."

### Prerequisites

- **pypandoc_binary** for `.docx` conversion (included in `requirements.txt`)

### What Gets Extracted

| Format | Content extracted |
| ------ | ---------------- |
| `.docx` | Full document converted to Markdown via Pandoc |
| `.pptx` | All slide text (titles, bullets, text boxes, tables) + speaker notes |
| `.md` | Read as-is |
| `.txt` | Read as-is |

Note: `.pptx` extraction reads text from shapes and tables. Text embedded in images, charts, or SmartArt is not extracted. Files in `.xlsx`, `.pdf`, and `.csv` format are skipped.

### What the importer does automatically

- Detects customer-first vs type-first directory layout
- Extracts **customer** from top-level directory name
- Infers **type** from subdirectory names (`Meetings/`→meeting, `QBR/`→meeting, `Opportunities/`→project, `RFP/`→project, `ESAT/`→esat)
- Extracts **dates** from filenames (`2025_11_14` → `2025-11-14`)
- Flags **archived** content from `Archived/` subdirectories
- Skips **duplicates** (Google Drive `(1)` copies)
- Skips **meta files** (`_notebook-instructions.txt`)
- Cleans **titles** (strips timestamps, version markers, Gemini suffixes)
- Tracks imported files to avoid duplicates on re-run

## AI Stack

The vault is designed for three layers of AI:

| Layer | Tool | Use Case |
| ----- | ---- | -------- |
| In-vault chat | **Obsidian Copilot** | Ask questions about your notes, generate content |
| Passive discovery | **Smart Connections** | Auto-surface related notes as you write |
| Power operations | **Cursor + Claude** | Bulk processing, reorganisation, content generation |

Configure API keys in the Copilot and Smart Connections plugin settings after opening the vault in Obsidian.

## Project Structure

```
vault-forge/
├── .cursor/rules/       Cursor AI rules for this project
├── setup_vault.py       Vault scaffolding script
├── import_notes.py      Local file import pipeline
├── config.yaml          All configuration
├── requirements.txt     Python dependencies
├── templates/           Obsidian template source files
├── prompts/             AI prompt template source files
├── obsidian_config/     .obsidian JSON configs
└── content/             Starter vault content
```
