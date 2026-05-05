# Vault Conventions

This guide documents the naming, tagging, and metadata rules for this vault. Consistent conventions are critical for Dataview queries, AI retrieval (RAG), and long-term maintainability.

## Note Types

Every note must have a `type` frontmatter property. Valid values:

`customer` | `person` | `meeting` | `project` | `knowledge` | `industry` | `competition` | `demo` | `esat` | `partner` | `workshop` | `certification` | `daily` | `weekly-review`

## Status Values

Where applicable, notes have a `status` property. Valid values:

`active` | `inactive` | `completed` | `archived` | `draft`

Status is always a frontmatter property, never a tag.

## File Naming

- **Evergreen notes**: Title Case with spaces. Example: `Acme Corp.md`, `Elastic APM Overview.md`
- **Dated notes**: `YYYY-MM-DD - Title.md`. Example: `2026-03-09 - Weekly Sync with Acme Corp.md`
- **Avoid**: `# | ^ : % [[ ]]` in filenames

## Folder Naming

- Numbered hyphenated prefixes: `01-Customers`, `02-Projects`
- Title Case after prefix
- Utility folders have no prefix: `Templates`, `Prompts`, `Assets`
- Maximum 3 levels of nesting

## Frontmatter Rules

- **Relationship fields use wikilinks**: `customer: "[[Acme Corp]]"` -- creates backlinks and enables Dataview queries
- **No blank properties**: If a field doesn't apply, omit it entirely
- **Dates**: ISO 8601 format `YYYY-MM-DD`
- **Aliases**: YAML list format for customers and people:
  ```yaml
  aliases:
    - Acme
    - ACME Corp
  ```

## Tags

Tags are for cross-cutting themes that span note types and folders:

`#security` | `#observability` | `#search` | `#migration` | `#performance`

Rules:
- Never duplicate what frontmatter captures (no `#meeting`, no `#acme`)
- Flat namespace only (no `#elastic/security`)
- No status tags

## Links

- Use wikilinks: `[[Acme Corp]]`, `[[Sarah Chen]]`, `[[Q1 Migration Project]]`
- Links are the primary organisational tool -- they build the knowledge graph
- Shortest path format (no folder paths in links)

## Headings

- H1 is the note title (matches filename)
- Body sections start at H2
- Never skip heading levels

## Maintenance Cadence

- **Weekly**: File or discard `00-Inbox/` notes. Run weekly review.
- **Monthly**: Run Find Orphaned Files. Check for broken links. Review archive.
- **Quarterly**: Audit customer statuses. Review tag taxonomy. Check for stale projects.
