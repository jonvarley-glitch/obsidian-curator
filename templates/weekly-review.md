---
type: weekly-review
date: <% tp.date.now("YYYY-MM-DD") %>
week-number: <% tp.date.now("ww") %>
---
# <% tp.file.title %>

## Wins

-

## Challenges

-

## This Week's Meetings

```dataview
TABLE customer, date
FROM "03-Meetings"
WHERE date >= date(today) - dur(7 days) AND date <= date(today)
SORT date DESC
```

## Completed Tasks This Week

```dataview
TASK
WHERE completion >= date(today) - dur(7 days) AND completed
LIMIT 30
```

## Inbox Review

- [ ] All `00-Inbox/` notes filed or discarded
- [ ] No unprocessed quick captures remaining

## Customer Status Check

- [ ] Active customer statuses still accurate
- [ ] Follow-ups sent where needed

## Next Week Priorities

1.
2.
3.
