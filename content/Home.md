# Home

[[Getting Started]] · [[Conventions]]

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

## Open Tasks

```dataview
TASK
WHERE !completed AND !contains(text, "Example:")
SORT due
LIMIT 20
```

## Overdue

```dataview
TASK
WHERE !completed AND due AND due < date(today)
SORT due
```

## ESATs

```dataview
TABLE customer, opportunity, status
FROM "08-ESATs"
WHERE type = "esat"
SORT date DESC
```

## Upcoming Deadlines

```dataview
TABLE provider, status, target-date
FROM "10-Certifications"
WHERE type = "certification" AND status != "completed"
SORT target-date
```
