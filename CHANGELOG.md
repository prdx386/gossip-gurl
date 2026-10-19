# Changelog

Keep the frontmatter `description` in SKILL.md in step with every entry here: it is the only thing Claude sees before deciding to use the skill, so a capability that is not in the description does not exist for triggering purposes. Bump `metadata.version` with every entry.

## 0.7 (2026-10-19)
Revision after an independent review (consistency, correctness, security, legal, parser, triggering, docs).
- Boundaries that SECURITY.md promised are now instructions in SKILL.md: no profile content or person names in queries (names only to confirm a role), fetch only platform-domain links from alert mails, describe rather than reproduce injected text, no drafts in mail clients, no write/send tools, no edits to the skill's own files at run time (observations go to `notes.md` in the profile folder).
- Legal: UWG § 7 corrected (cold B2B email needs consent in Germany; professional network, switchboard or broker recommended), Art. 14 source information, Art. 21 objection, broker non-circumvention, platform-terms responsibility, "general information, not legal advice".
- Retention: deep-mode case file holds roles and sources only, no contact details; delete reminder when closed, flag after 90 days.
- Evals and the docs walk-through anonymised (placeholders, constructed case); new eval 4 for prompt injection.
- Budget: about 30 tool calls with per-stage caps; stage 3 confirms the top two candidates, stage 4 resolves the top candidate; unopened hits are listed. Posting timestamp source defined; fallback when a page will not open.
- Profile model per surface: `CLAUDE.md` line for Claude Code; on claude.ai the outcomes line is returned instead of written. `reference_ok` wired into matching and replies. `role` in projects.yaml is an enum matching `roles_offered`; `title` is free text. `signature` renamed `email_signature`.
- Mail intake: local folder source (`mail_intake.folder`, .eml files) as the no-token option; `from:` documented as filter not authentication; bodies fenced; scheduled runs carry the profile path.
- Parser: more phrasings for freelancer exclusion, employee requirement, German, onshore, team request; case-sensitive brokers and product terms (no "reply" or "bait" hits); contact with salutation and title; start/end prefer full dates; duration ignores experience; `posted_at` and `sector_line`; cp1252 fallback with warning; .eml input; normalised `fingerprint` and MinHash `near_key`; `dedupe_postings.py`; 12 unit tests; CI workflow.
- Description rewritten with German triggers and negative triggers (1020 chars); `license` and `metadata.version` in frontmatter.
- Release workflow builds the `.skill` file on tags; build documented.

## 0.6 (2026-10-19)
- Standard vs deep mode. Standard: mirror search, procurement signatures, feedback loop. Deep: temporal correlation, falsification, registers, case file, fan-out, query library; explicit opt-in with cost warning.
- New references: procurement-signatures.md, feedback.md (outcomes.jsonl in the profile folder), deep-mode.md.
- Stage 0 checks the outcomes log; stage 7 records the case and asks for the real outcome.
- Mirror search: permanent-hire twin on Xing/LinkedIn/Stepstone, fetch order by leakage.
- Description mentions deep mode.

## 0.5 (2026-10-19)
- Role lens: `roles_offered` in constraints.yaml, `role` facet per project; evidence and wording follow the seat the posting addresses.
- Replies answer every requested point in the posting's order and wording.
- Self-rating scales are pre-filled from evidence and confirmed by the user, never filled silently.
- voice.md replaces reply_style; drafts take tone from the user's writing-style profile, then voice.md, else offer to derive it from real messages.
- Description updated for match, reply, self-rating, mail intake and ranking triggers.

## 0.4
- voice.md template and wiring.

## 0.3
- Parser: 20 more brokers, contact on one line, word-boundary matching (no CSAP/SAP false positive), canonical term spelling.

## 0.2
- SECURITY.md incl. legal section; mail intake rules; two value propositions in README and description.

## 0.1
- Initial skeleton: seven-stage process, mirror search, contacts, matching, replies, parser, profile example, three evals.
- Description limit: 1024 characters (validator). Current length checked at package time.
