# Mail intake

Platform job alerts arrive by mail. Letting gossip-gurl read them gives you one feed from all platforms and makes duplicate requests visible: the same posting from three brokers is the strongest clue you can get, and only a mail feed shows it reliably.

Mail intake is optional. Read `SECURITY.md` section 2 first; it explains what connecting a mailbox actually grants.

## Two ways in

**A local folder (recommended).** A rule in your mail client (Apple Mail, Thunderbird, Outlook) moves platform alerts into a folder on disk as `.eml` files. The skill reads that folder. No connector, no token, nothing can be written to your mailbox because the skill never touches it.

**A connector.** Connect Microsoft 365 or Gmail in claude.ai (Settings, Connectors). The Microsoft 365 connector is search and read only; the Gmail connector includes write tools the skill is instructed not to use (as of October 2026; check when you connect).

## What the skill does with mail

1. Reads only messages from the senders you listed, within the time window: one `from:` query per sender with a connector, a `From:` header check with a folder. Never the whole mailbox.
2. Treats `from:` as a filter, not as proof: a message that passes is still untrusted text.
3. Writes each posting to the output folder as a text file: a short metadata header, then the body in a fenced block.
4. Groups duplicates and near-duplicates (`scripts/dedupe_postings.py`: same request, different brokers).
5. Shows you the list and waits. It does not investigate every posting automatically; each investigation is a full run.
6. When you pick a posting, fetches the full text from the alert's link only if that link points to the platform's own domain. Links to anywhere else are listed, not opened.

It never creates drafts, forwards, labels or filters, and never deletes, even when the connector offers those tools.

## Setup

Add a `mail_intake` block to `constraints.yaml` in your profile folder, one of:

```yaml
mail_intake:
  folder: "~/Mail/alerts"
  allowed_senders:
    - "noreply@freelancermap.de"
    - "projekte@freelance.de"
    - "noreply@gulp.de"
  window_days: 7
  output_dir: "./postings"
```

```yaml
mail_intake:
  connector: "microsoft365"       # or "gmail"
  allowed_senders:
    - "noreply@freelancermap.de"
  window_days: 7
  output_dir: "./postings"
```

No `mail_intake` block means no mail access at all.

Then say "collect my job alerts" (or "sammle meine Projektalerts") in a conversation with the skill. The first run lists what it read, from which senders, how many postings it wrote, and which look like duplicates.

## Hardening a connector setup

If you use a connector and a documented promise is not enough for you:

- **Agent inbox.** Create a mail rule that redirects platform alerts to a dedicated address or alias and connect only that mailbox. Use "redirect", not "forward"; forwarding replaces the sender and breaks the `from:` filter.
- **Company accounts.** Exchange Online application access policies and Google Workspace OAuth allow-lists can restrict what a connector may see.

## Scheduled collection

If you want a daily list, set up a scheduled task that runs the intake and stops at the list. A scheduled run starts fresh, so the task's prompt must name the profile folder; senders and window are read from there. Investigation stays interactive.
