# Feedback loop

The skill gets better only if resolved cases flow back. Each time the user learns the real client (recruiter names it, the client answers, the mirror posting says it), record the outcome. This costs one line and pays twice: the next posting with the same fingerprint is recognised without a single search, and the confidence language calibrates against reality.

## Where

`outcomes.jsonl` in the user's profile folder (never in the skill or the repo). One JSON object per line:

```json
{"date": "2026-10-19", "fingerprint": "3adc3ac41c04", "near_key": "9f1c…", "title": "ISMS Assessment Consultant", "brokers": ["Broker A", "Broker B", "Broker C"], "predicted": "Example Utility GmbH", "predicted_confidence": 0.9, "confirmed": "Example Utility GmbH", "confirmed_by": "recruiter call", "notes": "freelancer exclusion applied at all brokers"}
```

`confirmed` may be `null` while open, or `"not disclosed"`. On a surface where nothing can be written, hand the line to the user in the reply and ask them to append it themselves.

## At the start of every run

Read `outcomes.jsonl` if it exists. If the new posting's `fingerprint` matches, or its `near_key` shares 60 % or more positions with a recorded one, or the requirement block reads near-identical: say so first ("Spotted before: same request, case of 2026-10-19, Example Utility"), reuse the result, and run only the steps the user still wants. Do not re-investigate a known case unless asked.

## At the end of every run

Append the case with `confirmed: null`. Then ask the user, once, to tell you the outcome when they learn it. When they do, update the line (`confirmed`, `confirmed_by`), and:
- if prediction and outcome agree, note it in the report of the next similar case as calibration evidence;
- if they disagree, say what misled you, and write the lesson into `notes.md` in the profile folder (a dated line: signature seen, what it turned out to be). Never edit `procurement-signatures.md` or `mirror-search.md` at run time: the skill directory is read-only on some surfaces and overwritten on update on others, and the repository must stay free of case data. A lesson that holds across cases goes upstream as a contribution (CONTRIBUTING.md).

## What not to record

Only the organisation and how the case was confirmed. No names of people, no contact details, no content of the user's conversations with the recruiter or client. The outcomes file is a calibration log, not a CRM.
