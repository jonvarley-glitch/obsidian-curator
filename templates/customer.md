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

```dataview
TASK
WHERE customer = this.file.link AND !completed
SORT due
```
