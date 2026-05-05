---
type: project
customer: "[[<% tp.system.prompt("Customer") %>]]"
status: active
start-date: <% tp.date.now("YYYY-MM-DD") %>
end-date:
---
# <% tp.file.title %>

## Objectives



## Scope



## Timeline

| Milestone | Date | Status |
| --------- | ---- | ------ |
|           |      |        |

## Meetings

```dataview
TABLE date, attendees
FROM "03-Meetings"
WHERE project = this.file.link
SORT date DESC
```

## Tasks

- [x] 

## Notes

