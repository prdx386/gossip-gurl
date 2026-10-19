# Installation

gossip-gurl is a Claude skill: a folder of instructions and small scripts that Claude reads when a conversation calls for it. It runs wherever Claude runs with web search. Nothing is installed on your machine beyond the folder.

## claude.ai (web, desktop, mobile)

1. Download the latest `gossip-gurl.skill` file from the Releases page of this repository (or build it yourself, see below).
2. Open claude.ai, drag the file into a conversation or attach it.
3. Claude shows a card with a **Save skill** button. Click it. The skill is now part of your profile and available in every new conversation.
4. To update, repeat with the newer file; the name stays the same, the old version is replaced.

Skill creation must be allowed on your account. On Team and Enterprise plans an administrator may need to enable it.

On claude.ai the skill has no persistent folder of its own: profile files are attached to a chat or kept in a Project, and the skill hands you anything it would otherwise write (the outcomes line) to keep yourself.

## Claude Code

Clone or copy the repository into your skills directory:

```bash
# personal, available in all projects
git clone https://github.com/<owner>/gossip-gurl ~/.claude/skills/gossip-gurl

# or project-scoped
git clone https://github.com/<owner>/gossip-gurl .claude/skills/gossip-gurl
```

Claude Code picks the skill up on the next session. `/gossip-gurl` invokes it directly; pasting a posting also triggers it. Here the skill can read and write a profile folder on disk; name it once in `CLAUDE.md` (`gossip-gurl profile: ~/gossip-gurl-profile`).

## Building the `.skill` file yourself

A `.skill` file is a zip archive with the skill folder at its root. From the parent directory of your checkout:

```bash
zip -r gossip-gurl.skill gossip-gurl -x 'gossip-gurl/.git/*' 'gossip-gurl/.github/*' '*__pycache__*' '*.skill'
```

The release workflow in `.github/workflows/release.yml` does the same on every `v*` tag and attaches the file to the GitHub release.

## Requirements

- Web search and web fetch must be available in the session. Without them the skill can parse and match but cannot find mirrors or people.
- Python 3.9 or newer is optional. The parser and dedupe scripts are a convenience; the skill works without them.
- A mail connector (Microsoft 365 or Gmail) or a local mail folder is optional and only needed for mail intake. Read `SECURITY.md` section 2 before connecting anything.

## First run

Paste a posting. That is all. The report comes back in the language of the posting.

For match scoring and reply drafts, set up a profile folder: see `docs/profile-setup.md`.
