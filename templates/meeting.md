---
type: meeting
date: <% tp.date.now("YYYY-MM-DD") %>
customer: "[[<% tp.system.prompt("Customer") %>]]"
project: "[[<% tp.system.prompt("Project (or leave blank)") %>]]"
attendees:
  - "[[<% tp.system.prompt("Attendees (comma-separated)") %>]]"
---
# <% tp.file.title %>

## Agenda

-

## Discussion



## Action Items

- [x] 

## Follow-ups

- [x] 
