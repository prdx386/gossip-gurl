# Drafting replies

Two audiences, two drafts. Both are drafts: the user sends them, the skill never does. Default to the language of the posting.

## Voice

Tone comes from the user, not from the skill:
1. If the session offers the user's own writing-style profile (a writing-style skill or memory of how they write), use that first.
2. Otherwise read `voice.md` in the profile folder. Its samples weigh more than its rules.
3. If neither exists, offer once to draft `voice.md` from two or three real messages the user pastes (anonymised by them). Write the draft, show it, and use it only after they have corrected it. Do not invent a voice from the CV.
The sign-off block and reference-article link come from `constraints.yaml` (`email_signature`, `reference_article_url`). Voice applies to drafts only; reports and match verdicts keep the skill's neutral tone. Where the session offers the user's writing-style profile and `voice.md` disagree, the writing-style profile wins; `voice.md` is the fallback for sessions without one.

## Pick the lens first

The same CV reads differently depending on the role the posting wants. Before drafting, decide which of the user's roles this posting is about (`constraints.yaml`, `roles_offered`, the same values as `role` in `projects.yaml`; the example profile uses `auditor`, `consultant`, `interim_ciso`, users add their own) and write everything from that seat:
- Auditor lens: independence, evidence methods, standards, number and type of audits, what you do not do (no implementation for the same client).
- Consultant lens: outcomes delivered, roadmaps, stakeholders, how you got things implemented.
- Interim/line lens: team size, budget, board reporting, incidents handled.
Pull projects from `projects.yaml` by the `role` value that fits the lens, not by recency. Clients with `reference_ok: false` are described, never named. If the posting mixes lenses (assessment plus implementation), lead with the one the must-haves weigh most. If it is unclear which lens the user wants, ask once; the lens changes every sentence, so guessing wastes the draft.

## To the recruiter: point by point

Recruiters and client procurement score against their own list. The reply therefore answers every requested point, in the posting's order, under the posting's wording, with one line of evidence each (project, sector, year, or certificate). Never summarise five points into one paragraph; never skip a point you fail. A failed point gets the honest status plus the mitigation (team partner, comparable experience, timeline to obtain).

Structure:
1. One line: which role, where seen, availability from when.
2. The requested administrative facts in the posting's order: availability, rate (or "on request" if the user prefers), focus area among the ones listed, legal form if asked.
3. The requirement block: every must-have and should-have as its own line, mirroring the posting's numbering or bullets, each with status and evidence. Keep the posting's own terms so a scorer finds them.
4. Close with the next step you want (call, CV attached, team partner named).

Length: as long as the requirement list needs, not longer. No marketing adjectives.

## Self-assessment scales

Many postings ask the applicant to rate themselves per requirement (1 to 10, A to D, years of experience per item, "Bitte bewerten Sie sich pro Punkt"). Never fill these in silently. Instead:
1. Build the table in the posting's exact format.
2. Pre-fill each row with a proposed value derived from `projects.yaml` and `certs.yaml`, with the evidence next to it.
3. Ask the user to confirm or change every value before the draft is final (`AskUserQuestion` if the session has it, otherwise list the rows and ask in the reply). A self-rating is the user's statement, not the skill's; an inflated 9 the user cannot back in the interview costs more than an honest 6.
4. Mirror the confirmed values into the reply exactly as the posting asked (table, list, or inline).

If the posting asks for a document format (CV as Word, a filled template), say so in the report and produce the content in that structure; the user converts or the docx skill does.

## To the end client (direct outreach)

Use only when stage 4 produced a verified person and the report recommends it. Lead with a professional hook that is not the posting: a talk they gave, a role change, a public initiative, a shared contact (only if the user confirms the contact agreed to be named). Mention the posting at most as a question ("Does this sit with you?") and never assert ownership. One sentence on what the user does that fits. One clear ask: a short call. The draft positions the user; it does not pitch for the broker's request past the broker (SECURITY.md section 4, broker contracts).

Channel: prefer a professional-network message or the published switchboard over a cold email; in Germany a cold business email needs prior consent (§ 7 UWG). If the user chooses email, the draft says in one clause where the user saw the person's role (conference programme, company page), which covers the Art. 14 GDPR source information and reads better than pretending.

Provide two variants where the culture is ambiguous (formal / informal address in German). If the channel is a connection request with a character limit, provide a version inside the limit and count the characters.

## What not to write

- No claims the profile cannot back.
- No reference to information the user found through research but the recipient did not publish (private details, internal org charts). Public is public; inferred stays in the report.
- No pressure or urgency phrasing.
