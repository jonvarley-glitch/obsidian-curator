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

```tasks
done
done after 7 days ago
sort by done reverse
limit 30
hide backlink
```

## Open Tasks Carried Over

```tasks
not done
due before today
sort by due
limit 20
hide backlink
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
