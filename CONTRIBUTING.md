# Contributing

gossip-gurl improves through observed cases, not through more rules. The most valuable contributions are small and factual.

## What helps most

1. **Procurement signatures** (`references/procurement-signatures.md`): a row describing how a client family buys, observed across at least two postings or one confirmed case. Group or sector level, dated, never a person.
2. **Platform behaviour** (`references/mirror-search.md`, table "What mirrors typically reveal"): what a platform or broker shows and omits. Dated.
3. **Evals** (`evals/evals.json`): a posting with recruiter and client names replaced by placeholders, with an expected outcome that describes the shape of a correct result rather than naming the real client.
4. **Parser fixes** (`scripts/parse_posting.py`): new broker names, date formats, constraint phrases. Add a case to `tests/test_parser.py` for every fix; the test postings are synthetic.
5. **Market adaptations**: a `platforms-<country>.md` for a market other than DACH, following the structure of the DACH table.

The skill never edits its own files at run time; observations it makes during a run land in `notes.md` in the user's profile folder. Bringing a general lesson from there into the repository is the contribution.

## Rules

- No personal data in the repo: no names of recruiters or client staff, no email addresses, no resolved real procurements, no outcomes logs, no profile folders. Anonymise before you paste.
- No scraping helpers, no login automation, no bulk collection. Pull requests that add them will be closed; see SECURITY.md section 5.
- Keep SKILL.md lean. New capability goes into a reference file; SKILL.md only gets the one line that says when to read it. A promise in SECURITY.md or the docs must have a matching instruction in SKILL.md or a reference.
- Every change to what the skill can do updates the frontmatter `description` (max 1024 characters), `metadata.version` and `CHANGELOG.md`.
- English for instructions and code; keep domain terms in their original language (e.g. "§ 8a BSIG").

## Testing a change

```bash
python3 -I -m unittest discover -s tests          # parser
python3 -I scripts/parse_posting.py evals/...      # or any posting file
```

Then install the skill locally (see docs/installation.md), paste the eval prompts from `evals/evals.json` into fresh conversations, and compare against `expected_output`. Eval 4 checks that injected instructions are reported and not followed.

## Releasing

1. Bump `metadata.version` in `SKILL.md` and add the entry to `CHANGELOG.md`.
2. Tag: `git tag v0.7.0 && git push --tags`. The release workflow builds `gossip-gurl.skill` and attaches it to the GitHub release.

## Reporting security issues

Use the repository's private vulnerability reporting (Security tab, "Report a vulnerability"), without real postings or personal data. Do not open a public issue for anything that exposes data.
