# How a run works

You paste a posting. gossip-gurl treats it as a case and works through seven stages. This page shows what happens in each and what the report looks like. The case below is constructed from the patterns of several real ones; the organisation, people and dates are invented.

## The case

A posting from a staffing broker: "ISMS and OT security assessment, ISO 27001 / KRITIS, Hanover, 70 % remote, start 1 December, about 30 person-days, team bids welcome, must-haves include audit competence under § 8a BSIG and an active ISO 27001 Lead Auditor certification." No client named.

## Stage 0: known case?

If your profile folder has an outcomes log, the skill checks whether this request has been seen before. Four brokers pushed this one within a day; after the first run, the next three were recognised in seconds.

## Stage 1: parse

The parser extracts broker, contact, posting date, start, end, person-days, remote share, cities, certifications, framework terms and procurement constraints. The skill then reads for what a script cannot see: the phrase "central security requirements and decentral units" (a group with subsidiaries), the sector doublet "transport and logistics" in the references wanted (describes the client, not the market), and anything inconsistent (a framework from another sector, a start date in the past) that becomes a question for the recruiter.

## Stage 2: mirrors

The same request usually exists at other brokers. The skill searches with distinctive phrases, numbers and platform names, opens the plausible hits and compares. In this case: three more brokers within 24 hours, and one variant described the client in a single sentence as the IT subsidiary of a public transport group. Another variant carried the condition "freelancers excluded, employee required". Different brokers, different leaks. One hit would not open (login wall); the report lists it as not opened.

## Stage 3: candidates

Constraints, broker count and timing are compared against the procurement-signature table (panel of brokers plus freelancer exclusion points to one group's procurement). Then candidates are listed with evidence. Here the mirror sentence fit exactly one organisation in Hanover; it was marked verified, with the sentence quoted.

## Stage 4: people

Sponsor from the management page (the executive responsible for IT, in office since spring, which fits the pattern of a new executive commissioning an independent benchmark), owner from job ads and conference lists (an information security officer, an OT security team), group layer from the parent's annual report and speaker bios. Every name carries its source and the source's date. The email pattern comes from the company's own contact pages and is labelled unverified.

## Stage 5: fit and reply (with a profile)

The requirement list becomes a matrix in the posting's own order, each row with status and evidence from `projects.yaml` and `certs.yaml`. Formal hurdles (legal form against the exclusion rule, dates against commitments) sit above the matrix because they decide more. Verdict in three levels: apply, only as part of a team, skip. Here: "only as part of a team" (OT depth missing, one-person company excluded), with the partner profile named. The reply draft answers every requested point in order, in your voice, and names the gap with the mitigation.

## Stage 6: the report

```
## Spotted
Nordstadt Verkehrs-IT GmbH, Hanover. Probability 90 %. Fourth broker for the same request.

## Verified
- Posting #…, published 12.11., sector "transport", team request (posting text)
- One mirror describes the client as the IT subsidiary of a public transport group (platform, 13.11.)
- One mirror excludes freelancers and requires employment (platform, 13.11.)
- Hit at <platform> not opened (login wall); snippet matches the title and city

## Inferred
- Four brokers in 24 h: central procurement with a supplier panel. Confidence high.
- "IT subsidiary of a public transport group" with seat in Hanover fits one organisation. Confidence high.
- Year-end management presentation plus benchmark: commissioned at executive level. Confidence medium.

## Candidates
1. Nordstadt Verkehrs-IT GmbH, 90 %. Evidence: … What would rule it out: a second transport group IT subsidiary in the region (none found in 2 searches).

## People
Sponsor: A. Example, Managing Director IT and Operations, since spring 2026 (company site, 2026)
Owner: B. Example, Information Security Officer (public profile snippet, 2026); OT security team (job ad, 2026)
Group: C. Example, Group CISO (conference programme, 2026)
Email pattern: first.last@<domain>, from company contact pages; individual addresses unverified.

## Fit and hurdles
Hurdle: one-person company vs. exclusion rule. Matrix: 6 met, 1 partial, 1 missing (IEC 62443 depth). Verdict: only as part of a team.

## Recommended next step
Contact the owner through a professional-network message with a professional hook (talk, role change), not the posting; say where you saw their role. Ask the recruiter whether the exclusion rule applies at this broker and whether the OT part may be covered by a partner. Apply through the broker if you apply at all.
```

## Stage 7: verify and record

Before delivering, the skill re-reads: does every name have a source and a date? Is anything stated as fact on one secondary source? Did the first idea become the top candidate by inertia? Then it appends the case to your outcomes log (or hands you the line if it cannot write) and asks you, once, to report the real client when you learn it.

## Standard and deep

What you just read is standard mode: about 30 searches, fetches and file reads, with a cap per stage. Say "deep" or "gründlich" and the skill adds temporal correlation (the client's own job ads and tenders in the weeks before), falsification searches for the top candidate, register sources, a case file and parallel candidate research. It tells you the cost first. Most cases do not need it.

## When the trail is cold

A posting with no sector, no location, no regulation terms and generic requirements leaves nothing to follow. The skill says so after stage 3, lists the two or three questions to ask the recruiter, and stops. A short "no trace" is worth more than a long guess.
