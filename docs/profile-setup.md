# Profile folder

Without a profile, gossip-gurl tells you who is behind a posting. With a profile, it also tells you whether the posting fits you and drafts the reply. The profile is a folder of plain files on your side; the skill reads it when you point to it and is instructed never to put its contents into a search query or a web request (`SKILL.md`, Boundaries).

## Create it

Copy `assets/profile.example/` to a location outside the skill and outside any repository, for example `~/gossip-gurl-profile/`. Then fill in the five files.

| File | What goes in | Read when |
|---|---|---|
| `constraints.yaml` | Legal form, roles you offer, availability, commitments, onsite limit, rate policy, sign-off block, optional mail intake | Start of every run (mail configuration, formal hurdles) |
| `cv.md` | Your CV as free text: summary, positions, education, publications, talks | Match and reply only. Gives context and tone; nothing here is used as evidence. |
| `projects.yaml` | One entry per project: client (may be anonymised), sector, the role you held, period, frameworks, OT scope, whether the client may be named | Match and reply only. This is the evidence base; every "met" in the matrix cites an entry here. |
| `certs.yaml` | Active certifications with issuer and validity; expired ones separately | Match and reply only. "Active certification required" is checked here; expired ones are never listed as current. |
| `voice.md` | How you write to business contacts, with two or three real messages as samples | Reply drafts only. If missing, the skill offers once to draft it from messages you paste. |

The skill also keeps `outcomes.jsonl` (see below), `notes.md` (its own observations about platforms and procurement patterns), and in deep mode `cases/<fingerprint>.json` in this folder.

## The role facet

`constraints.yaml` lists the roles you apply from (`roles_offered`), for example `auditor`, `consultant`, `interim_ciso`; add your own. Each entry in `projects.yaml` has a `role` field with one of those same values (and a free-text `title` for display). The skill picks one lens per posting and pulls evidence by that value: a project you did as auditor is not quoted as implementation experience, and the reply is written from the auditor's seat (independence, evidence methods, number of audits) rather than the consultant's (outcomes, roadmaps, stakeholders).

## Anonymising clients

Set `reference_ok: false` on any project whose client may not be named to recruiters. The skill then cites it as "regional energy utility (KRITIS), audit 2024" in the matrix and in every draft, never by name. Sector, role, period and frameworks must still be real; the match depends on them.

## Pointing the skill at it

Say once per conversation where the folder is ("mein Profil liegt unter ~/gossip-gurl-profile"). In Claude Code, a line in `CLAUDE.md` saves repeating it:

```
gossip-gurl profile: ~/gossip-gurl-profile
```

On claude.ai without a persistent folder (files attached to a chat or a Project), the skill reads the files but cannot write back: it hands you the outcomes line to paste into your log, and mail intake stops at the list.

## The outcomes log

The skill keeps `outcomes.jsonl` in the same folder: one line per case with the predicted and the confirmed end client. It is what makes the skill recognise a posting it has seen before and what calibrates its confidence over time. Tell the skill the real outcome when you learn it. The log holds organisations and confirmation sources only, no people. See `references/feedback.md`.

## Deep-mode case files

In deep mode the skill writes `cases/<fingerprint>.json` with the research so a follow-up question does not repeat it. It contains roles, organisations and sources, no contact details. It is still personal data: delete it when the case is closed. The skill reminds you, and flags case files older than 90 days.

## What stays out

Do not put passwords, API keys, bank details or anything you would not show a recruiter into the profile folder. The skill does not need them, and a folder that only holds professional data is a folder you can hand to the skill without a second thought.
