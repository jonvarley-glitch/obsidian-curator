---
type: daily
date: <% tp.date.now("YYYY-MM-DD") %>
---
# <% tp.file.title %>

## Focus

-

## Meetings

-

## Notes



## Tasks

- [x] 

### Due Today

```dataview
TASK
WHERE !completed AND due = date(today)
```

### Overdue

```dataview
TASK
WHERE !completed AND due AND due < date(today)
```

## End of Day Review

