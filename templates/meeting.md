<%*
const customer = await tp.system.prompt("Customer");
const project = await tp.system.prompt("Project (blank for none)");
const attendees = await tp.system.prompt("Attendees (comma-separated)");
const projectLine = project ? `project: "[[${project}]]"\n` : "";
const attendeesLine = attendees
  ? `attendees:\n${attendees.split(",").map(a => `  - "[[${a.trim()}]]"`).join("\n")}\n`
  : "";
-%>
---
type: meeting
date: <% tp.date.now("YYYY-MM-DD") %>
customer: "[[<% customer %>]]"
<% projectLine %><% attendeesLine -%>status: active
---
# <% tp.file.title %>

## Agenda

-

## Discussion



## Action Items

- [ ]

## Follow-ups

- [ ]
