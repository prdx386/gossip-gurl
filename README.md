# gossip-gurl

*Spotted: an anonymous project posting.*

gossip-gurl is a Claude skill for freelancers. It does two things.

**It tells you who is behind a posting.** Staffing brokers anonymise their clients. gossip-gurl finds the same request at other brokers (each one leaks a different detail), reads the procurement rules, narrows the field and names the end client with an honest confidence level. Then it resolves the decision makers from public sources, every name with a source and a date. You talk to the right person instead of waiting in a recruiter's queue.

**It takes the grind out of the freelance pipeline.** Alerts from five platforms, the same request three times under different broker names, requirement lists to check against your CV by hand, and a reply to write every time. gossip-gurl collects the alerts, groups duplicates, scores each posting against your profile with the gaps spelled out, and drafts the reply in your voice, answering every requested point in the posting's own order. You decide and send. It never sends anything.

Built on the German-speaking freelance market (freelancermap, freelance.de, GULP, Hays, Experis and the like). The process is sector- and country-neutral; the experience tables are DACH and grow with reported cases.

## Quick start

1. Install: download `gossip-gurl.skill` from Releases and save it in claude.ai, or clone this repo into `~/.claude/skills/` for Claude Code. Details in [docs/installation.md](docs/installation.md).
2. Paste a posting into a conversation. That is the whole input. The report comes back in the posting's language.
3. Optional: set up a [profile folder](docs/profile-setup.md) for match scoring and reply drafts, and [mail intake](docs/mail-intake.md) for a single feed of all your job alerts.

## What a report looks like

```
## Spotted            who it most likely is, with probability
## Verified           facts with sources
## Inferred           conclusions with reasoning and confidence
## Candidates         ranked, with evidence and what would rule them out
## People             sponsor, owner, group layer; role, source, date
## Fit and hurdles    requirement matrix and verdict (with a profile)
## Recommended next step
```

A full walk-through on a constructed case: [docs/how-a-run-works.md](docs/how-a-run-works.md).

## Principles

- **Public, professional information only.** Company sites, job ads, annual reports, conference programmes, public directories, search snippets. No logins, no scraping, no private data.
- **Your data stays yours.** Queries are built from the posting and organisation names; nothing from your CV or project list goes into a search or a web request.
- **Evidence, not vibes.** Every name carries a source and a date. Inferred stays labelled inferred. "Verified" means a source said it.
- **You are the controller.** The results are personal data you are responsible for handling lawfully (GDPR, platform and broker terms, anti-spam rules). [SECURITY.md](SECURITY.md) section 4 says what that means in practice, including why cold email is the wrong channel in Germany.
- **Drafts are drafts.** There is no send step, and nothing is created in your mail client.
- **Lean by default.** A standard run is about 30 tool calls with a cap per stage. Deep mode exists, costs several times that, and asks first.

## Documentation

| | |
|---|---|
| [docs/installation.md](docs/installation.md) | claude.ai and Claude Code, requirements, first run, building the package |
| [docs/profile-setup.md](docs/profile-setup.md) | the profile folder: CV, projects, certifications, constraints, voice |
| [docs/how-a-run-works.md](docs/how-a-run-works.md) | the seven stages with an example report |
| [docs/mail-intake.md](docs/mail-intake.md) | collecting job alerts from a folder or a mailbox, and the hardening options |
| [docs/faq.md](docs/faq.md) | legality, confidence, cost, scope |
| [SECURITY.md](SECURITY.md) | security briefing: untrusted input, mailbox scopes, profile data, the law, boundaries |
| [CONTRIBUTING.md](CONTRIBUTING.md) | what helps most, the rules, releasing |
| [CHANGELOG.md](CHANGELOG.md) | versions |

## Layout

```
SKILL.md                      the process Claude follows, and the boundaries it keeps
references/
  mirror-search.md            finding the same posting at other brokers
  procurement-signatures.md   how client families buy, as seen in postings (observed table)
  contacts.md                 resolving people: source hierarchy, dating, email patterns, channel
  feedback.md                 outcomes log; recognising known cases, calibrating confidence
  matching.md                 requirement matrix, role lens, verdict
  replies.md                  recruiter reply, direct outreach, self-rating scales, voice
  intake-mail.md              mail intake rules (folder or connector)
  deep-mode.md                optional expensive steps
scripts/
  parse_posting.py            posting text or .eml -> structured JSON, fingerprint, near_key
  dedupe_postings.py          group a folder of postings into duplicates and mirrors
assets/profile.example/       copy outside the repo and fill in
evals/evals.json              test prompts with expected outcomes (anonymised)
tests/test_parser.py          parser tests (python3 -I -m unittest discover -s tests)
```

## Status

0.7, early. Built from real cases in the German security consulting market in October 2026, reviewed once by an independent pass for consistency, security and legal framing. Contributions welcome, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
