# Home

[[Getting Started]] · [[Conventions]]

> Browse: [[Task Board]] · [[Bases/Customers|Customers]] · [[Bases/Meetings|Meetings]] · [[Bases/Projects|Projects]] · [[Bases/Systems|Systems]]

## Active Customers

```dataview
TABLE industry, tier, status
FROM "01-Customers"
WHERE type = "customer" AND status = "active"
SORT tier
```

## Recent Meetings

```dataview
TABLE customer, date
FROM "03-Meetings"
WHERE type = "meeting"
SORT date DESC
LIMIT 10
```

## Active Projects

```dataview
TABLE customer, status, start-date, end-date
FROM "02-Projects"
WHERE type = "project" AND status = "active"
SORT start-date DESC
```

## Active Systems

```dataview
TABLE vendor, category, owner
FROM "04-Knowledge"
WHERE type = "system" AND status = "active"
SORT file.name
```

## Open Tasks

```tasks
not done
sort by due
limit 20
hide backlink
```

## Overdue

```tasks
not done
due before today
sort by due
hide backlink
```

## Due This Week

```tasks
not done
due before in 7 days
due after yesterday
sort by due
hide backlink
```

## Upcoming Deadlines

```dataview
TABLE provider, status, target-date
FROM "10-Certifications"
WHERE type = "certification" AND status != "completed"
SORT target-date
```
