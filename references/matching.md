# Matching a posting against the user's profile

Only run this stage when the user has pointed to a profile folder. The folder follows `assets/profile.example/`: `cv.md`, `projects.yaml`, `certs.yaml`, `constraints.yaml`. Read all four; the YAML files are what make claims checkable.

## Why a matrix, not a score

A single percentage hides the one hurdle that makes an application pointless (a required certification, an excluded legal form) behind nine things that fit. Recruiters read against a checklist, so the output mirrors their checklist.

## Pick the lens

Decide which of the user's offered roles (`constraints.yaml`, `roles_offered`) the posting addresses: the same project counts as evidence differently for an auditor, an implementation consultant or an interim CISO. Each entry in `projects.yaml` carries a `role` value from that same list (its free-text `title` is for display). Pull evidence by that value: a project held as `auditor` is not evidence of implementation experience. Score from that seat and say which lens you used; if two fit, show the verdict for both in one line each.

## Build the matrix

For every requirement in the posting, in the posting's own order:

| Requirement (as written) | Status | Evidence from profile |
|---|---|---|
| ISO 27001 auditing, 5+ years | met | projects.yaml: certification-body audits 2019-2026 |
| OT/ICS security, 3+ years, IEC 62443 | partial | projects.yaml: 2 KRITIS energy audits incl. OT scope, no 62443 lead role |
| Lead Implementer certification | missing | certs.yaml has Lead Auditor only |

Status values: met, partial, missing, unclear (profile does not say). Cite the file and entry; if you cannot cite, the status is unclear, not met. Cite a project with `reference_ok: false` by sector, role and year ("regional energy utility (KRITIS), audit 2024"), never by client name, in the matrix and in every draft.

## Formal hurdles, separately

Check `constraints.yaml` against the posting's constraints from `parse_posting.py`: legal form (one-person company vs. "freelancers excluded"), employee-required rules, onsite share vs. the user's maximum, date range vs. existing commitments, rate corridor vs. any stated budget, language. One failed hurdle is reported above the matrix because it decides more than the matrix does.

## Verdict

Three levels, with one sentence of reasoning:
- apply: all must-haves met or partial with a credible story, no formal hurdle.
- only as part of a team: one or two must-haves missing that a named partner type would cover (e.g. an OT specialist), posting allows team bids.
- skip: a formal hurdle fails, or the core of the role is a different profile (e.g. an operational SIEM analyst role for a governance person).

Say what would change the verdict (a certification, a partner, a clarification from the recruiter).

## Honesty rules

Never upgrade partial to met because the user would like it. Never list a certification that is not in certs.yaml or has expired. If the posting's numbers look like recruiter prose ("up to 18 years"), say so instead of scoring against them.
