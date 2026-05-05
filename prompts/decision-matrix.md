---
type: prompt
title: Decision Matrix
---

Help me build a weighted decision matrix for the technical choice described in the current note (or that I describe in chat).

Produce:

1. **Options** — a clear list of the candidate solutions / vendors / patterns.
2. **Criteria with weights** — propose 5-8 evaluation criteria appropriate to the decision (e.g. cost, fit, scalability, operational burden, security, lock-in). Assign each a weight from 1-5.
3. **Scored table** — score each option against each criterion (1-5) with a one-line rationale per cell. Include a Weighted Total column.
4. **Recommendation** — name the leading option, summarise why, and call out the strongest counter-argument.
5. **Open questions** — anything you couldn't score with confidence and would want to validate.

Render the matrix as a Markdown table. Cite vault notes (`[[Note Title]]`) when scoring is informed by something already captured. Where vault data is thin, flag it as an assumption rather than fabricating a score.
