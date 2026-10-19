# Finding mirror postings

Brokers receive the same request from a client's procurement and republish it with their own wording and omissions. Finding the mirrors is the single highest-yield step because each broker drops different details.

## Query patterns

Search three to five times, varying the anchor. Use quotes around phrases that are unlikely to appear elsewhere. Queries contain posting text, platform names and organisation names only; nothing from the user's profile.

1. A distinctive requirement phrase: `"Prüfverfahrenskompetenz nach § 8a"`, `"MITRE ATT&CK for ICS"`, `"CENELEC TS 50701"`.
2. Role title plus city plus month: `"Assessment Consultant" Frankfurt November 2026`.
3. Numbers: person-days plus start date, e.g. `40 Personentage 05.11.2026`.
4. Platform-scoped: the same phrases combined with `freelance.de`, `freelancermap`, `gulp`, `nexus.webconia.de`, `hays`, `solcom`, `westhouse`.
5. The broker's own listing page (platform company profiles list all their current postings).
6. The permanent-hire twin: clients often post the same role as a job ad under their own name in the same weeks. Search the role title plus city on Xing, Stepstone and the candidates' own career pages. LinkedIn Jobs only through search snippets; do not fetch linkedin.com. A named job ad with the same requirement list ends the case.

Fetch order when several hits appear: Nexus and freelance.de first (they show sector and client description), then GULP, then freelancermap and Experis/Hays variants (full text, fewer client clues). Budget: up to six fetches. Open the hits most likely to carry a client description first.

## When a page will not open

Several platforms render client-side, redirect to a login or block fetchers. If a fetch returns no posting text, use the search snippet for what it shows, list the URL in the report as "not opened", and move on. Do not retry with other tools or try to get around a login.

## What mirrors typically reveal (DACH market, observed October 2026)

| Platform / broker | Shows | Omits |
|---|---|---|
| freelance.de | first paragraph of the client description (often sector or a one-line client characterisation), start/end month, remote flag | company name behind paywall |
| nexus.webconia.de | third-party site that mirrors freelance.de postings with sector tag, legal-form rule, remote share, broker name and the broker's other postings; standing unclear, treat as a lead and confirm on the platform | nothing beyond the source |
| freelancermap | full text, broker, named recruiter, remote share | sector tag is often wrong (category chosen by recruiter) |
| GULP / Randstad Professional | full text, often matrix-generated prose | exclusive mandates rarely mirrored elsewhere |
| Experis, Hays, Westhouse, Solcom | full task list | procurement constraints the client imposed |

This table is experience, not documentation, and drifts. Note what you observe in `notes.md` in the profile folder; general lessons go to the repository through a contribution, never into this file at run time.

## Reading the mirror set

- Same text, 3+ brokers, posted within 24 hours: client procurement with a supplier panel. Large group, formal purchasing, probably a framework contract per broker. The strictest constraint among the variants is the real one. Without posting dates, compare by week and say that the timing clue is weaker.
- One broker, no mirrors after five varied searches: exclusive mandate. Note it in the report; the recruiter will name the client in a qualification call, so recommend that route.
- Variants that differ in duration or scope: the client is still shaping the request, or brokers are inventing. Report the range.

## Stop condition

Five varied searches without a new hit means there are no mirrors to find. Move on; do not keep rephrasing.
