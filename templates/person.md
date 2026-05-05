---
type: person
aliases:
  - <% tp.system.prompt("Short name or alias") %>
customer: "[[<% tp.system.prompt("Customer") %>]]"
role: <% tp.system.prompt("Role / Title") %>
---
# <% tp.file.title %>

## About



## Priorities and Interests



## Interaction History

```dataview
TABLE date, type
FROM "03-Meetings"
WHERE contains(attendees, this.file.link)
SORT date DESC
LIMIT 15
```
