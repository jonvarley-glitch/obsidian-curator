---
type: project
customer: "[[<% tp.system.prompt("Customer") %>]]"
status: active
start-date: <% tp.date.now("YYYY-MM-DD") %>
end-date:
---
# <% tp.file.title %>

## Objectives

-

## In Scope

-

## Out of Scope

-

## Stakeholders

| Name | Role | Side | Influence |
| ---- | ---- | ---- | --------- |
|      |      |      |           |

## Architecture

![[<% tp.file.title %> - Architecture.excalidraw]]

## Timeline

| Milestone | Date | Status |
| --------- | ---- | ------ |
|           |      |        |

## Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
| ---- | ---------- | ------ | ---------- | ----- |
|      |            |        |            |       |

## Decisions Log

Capture decisions inline as `### YYYY-MM-DD - Decision Title` so they remain searchable.

### YYYY-MM-DD - Example Decision

- **Context:**
- **Options considered:**
- **Decision:**
- **Consequences:**

## Meetings

```dataview
TABLE date, attendees
FROM "03-Meetings"
WHERE project = this.file.link
SORT date DESC
```

## Tasks

- [ ]

## Notes

