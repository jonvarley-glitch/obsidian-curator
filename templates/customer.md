---
type: customer
aliases:
  - <% tp.system.prompt("Short alias (e.g. Acme)") %>
industry: <% tp.system.prompt("Industry (e.g. Financial Services, Healthcare, Retail)") %>
status: active
tier: <% tp.system.prompt("Tier (e.g. Strategic, Growth, Standard)") %>
---
# <% tp.file.title %>

## Overview



## Key Contacts

| Name | Role | Notes |
| ---- | ---- | ----- |
|      |      |       |

## Architecture Overview

![[<% tp.file.title %> - Architecture.excalidraw]]

## Key Systems

```dataview
TABLE vendor, category, owner, status
FROM "04-Knowledge"
WHERE type = "system" AND customer = this.file.link
SORT file.name
```

## Meetings

```dataview
TABLE date, project
FROM "03-Meetings"
WHERE customer = this.file.link
SORT date DESC
LIMIT 20
```

## Projects

```dataview
TABLE status, start-date, end-date
FROM "02-Projects"
WHERE customer = this.file.link
SORT start-date DESC
```

## People

```dataview
TABLE role
FROM "01-Customers"
WHERE customer = this.file.link AND type = "person"
SORT file.name
```

## Open Tasks

<!--
Captures any incomplete task that either (a) mentions this customer by literal
wikilink in its text, or (b) lives in a note whose path contains the customer
name (e.g. dated meetings like `2026-03-09 - <Customer> - Topic.md`). Aliases
in task text are not matched -- write `[[<Customer>]]` exactly to surface the
task here.
-->

```tasks
not done
(description includes [[<% tp.file.title %>]]) OR (path includes <% tp.file.title %>)
sort by due
hide backlink
```
