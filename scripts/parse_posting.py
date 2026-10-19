#!/usr/bin/env python3
"""Parse a raw project/job posting into structured JSON.

Usage:
    python3 -I parse_posting.py posting.txt            # JSON to stdout
    python3 -I parse_posting.py alert.eml -o out.json  # .eml: headers + text body are read

Heuristic and deliberately conservative: it extracts what regexes can find
reliably (dates, person-days, remote share, certifications, procurement
constraints) and leaves interpretation to the model. Fields it cannot find
are null, never guessed. A `false` constraint means "phrase not recognised",
not "not required": the model reads the posting itself.

Two dedupe keys:
    fingerprint  exact match after normalisation (whitespace, wrapping, NBSP,
                 broker and contact lines removed): the same posting re-sent.
    near_key     MinHash of 5-word shingles, 32 positions as hex pairs. Two
                 postings sharing >= 60 % of positions are the same request
                 from different brokers.

No dependencies beyond the standard library.
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from email import policy
from email.parser import BytesParser
from pathlib import Path

# --- dates and numbers -------------------------------------------------------

DATE = r"\d{1,2}\.\d{1,2}\.\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{4}"
DATE_RE = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b")
MONTH_RE = re.compile(r"\b(0?[1-9]|1[0-2])/(\d{4})\b")
START_RE = re.compile(r"(?:Projektstart|Startdatum|Starttermin|Start|Beginn|ab)\s*:?\s*(?:ab\s+)?(" + DATE + r")", re.I)
END_RE = re.compile(r"(?:Projektende|Enddatum|Ende|Laufzeit\s+bis|bis(?:\s+zum)?)\s*:?\s*(" + DATE + r")", re.I)
POSTED_RE = re.compile(
    r"(?:ver[öo]ffentlicht|eingestellt|online\s+seit|erstellt|posted|published|Datum)\s*(?:am|on)?\s*:?\s*("
    + DATE + r")", re.I)
PT_RE = re.compile(r"(?:ca\.?\s*|rund\s*|etwa\s*)?(\d{1,4})\s*(?:PT\b|Personentage|Manntage|person[- ]days)", re.I)
REMOTE_RE = re.compile(r"(?:Remote(?:-?Anteil)?\s*:?\s*(\d{1,3})\s*%|(\d{1,3})\s*%\s*Remote)", re.I)
# Duration: a duration word nearby, or a bare "N Monate" at a field boundary (", 6 Monate,").
# "mind. 36 Monate Erfahrung" matches neither, so experience is not taken for project length.
NOT_EXPERIENCE = r"(?!\s*(?:Erfahrung|Berufserfahrung|Praxis|Projekterfahrung))"
DURATION_RE = re.compile(
    r"(?:(?:Dauer|Laufzeit|Projektdauer|Einsatzdauer|Zeitraum|zun[äa]chst(?:\s+für)?|für|über)\s*:?\s*"
    r"(?:ca\.?\s*|rund\s*|etwa\s*)?(\d{1,2})\s*(?:\+\s*)?Monat(?:e|en)?\b" + NOT_EXPERIENCE + r"|"
    r"(?:^|[,;|])\s*(?:ca\.?\s*)?(\d{1,2})\s*(?:\+\s*)?Monat(?:e|en)?\b" + NOT_EXPERIENCE + r")", re.I | re.M)
SECTOR_RE = re.compile(r"(?:Kategorie|Branche|Sektor|Industry|Sector)\s*:\s*([^\n]{3,120})", re.I)

# --- vocabularies ------------------------------------------------------------

CERTS = [
    "CISSP", "CISM", "CISA", "CRISC", "GCIH", "GCFA", "CySA\\+", "CSA",
    "ISO ?/?(?:IEC)? ?27001 Lead Auditor", "Lead Auditor", "Lead Implementer",
    "T\\.I\\.S\\.P\\.", "OSCP", "GICSP", "ITIL", "PMP", "PRINCE2", "Scrum Master",
]
CERT_RE = re.compile(r"(?<![A-Za-z])(?:" + "|".join(CERTS) + r")(?![A-Za-z])", re.I)

# Case-insensitive: regulation and standard names whose casing varies in postings.
FRAMEWORK_TERMS_CI = [
    "NIST CSF", "ISO/IEC 27001", "ISO 27001", "ISO 27002", "ISO 27019", "IEC 62443",
    "ISA/IEC 62443", "MITRE ATT&CK", "TIBER-EU", "KRITIS", "NIS2", "NIS-2", "§ ?8a",
    "BSIG", "TISAX", "CENELEC", "TS 50701", "SIEM", "MSSP",
]
# Case-sensitive: acronyms and product names that collide with ordinary words.
FRAMEWORK_TERMS_CS = [
    "DORA", "BAIT", "VAIT", "B3S", "SzA", "SOC", "Splunk", "QRadar", "Elastic", "Sentinel",
    "SAP", "S/4HANA", "Salesforce", "ServiceNow",
]
FRAMEWORK_RE_CI = re.compile(r"(?<![A-Za-z])(?:" + "|".join(FRAMEWORK_TERMS_CI) + r")(?![A-Za-z])", re.I)
FRAMEWORK_RE_CS = re.compile(r"(?<![A-Za-z])(?:" + "|".join(FRAMEWORK_TERMS_CS) + r")(?![A-Za-z])")
CANON = {t.lower().replace(" ", ""): t for t in FRAMEWORK_TERMS_CI + FRAMEWORK_TERMS_CS}

# Procurement constraints. Several phrasings each; still heuristic.
CONSTRAINTS = {
    "freelancers_excluded":
        r"(?:Freelancer|Freiberufler|Selbst(?:st)?ändige|1-Personen-Gesellschaft\w*|Ein-?Personen-?Gesellschaft\w*|"
        r"Einzelunternehm\w*|Solo-?Selbst\w*)[^.\n]{0,60}(?:ausgeschlossen|nicht möglich|nicht zugelassen|nicht erlaubt|"
        r"leider nicht|nicht gewünscht)|"
        r"\bkeine?\s+(?:Freelancer|Freiberufler|Selbst(?:st)?ändige)|"
        r"\b(?:nur|ausschließlich)\s+(?:ANÜ|Arbeitnehmerüberlassung|Festanstellung|sozialversicherungspflichtig)",
    "employee_required":
        r"sozialversicherungspflichtig|Arbeitnehmerüberlassung|\bANÜ\b|Festanstellung\s+(?:erforderlich|zwingend|notwendig)",
    "team_request":
        r"Teamanfrage|Expertenteam\w*|Teambewerbung\w*|Team-?Angebot\w*|als\s+Team\b|"
        r"im\s+Team\s+(?:vollständig\s+)?(?:abzudecken|abgedeckt|abdecken)",
    "onshore_only":
        r"\bOnshore\b|kein\s+Offshore|no\s+offshore|"
        r"(?:Leistungserbringung|Tätigkeit|Remote(?:-?Arbeit|-?Anteil)?|Arbeit(?:en)?)[^.\n]{0,30}"
        r"(?:nur|ausschließlich)?\s*(?:innerhalb|aus|in)\s+Deutschland|"
        r"(?:nur|ausschließlich)\s+aus\s+Deutschland",
    "german_required":
        r"(?:Deutsch(?:kenntnisse)?|German)[^.\n]{0,40}(?:verhandlungssicher|sehr gut|fließend|C1|C2|Muttersprach)|"
        r"(?:verhandlungssicher\w*|sehr\s+gute\w*|fließend\w*|muttersprachlich\w*|C1|C2)[^.\n]{0,25}(?:Deutsch|German)|"
        r"(?:Projekt|Dokumentations|Arbeits)(?:-\s*und\s+Dokumentations)?sprache\s*:?\s*(?:ist\s+)?Deutsch",
}

STRUCTURE_HINTS = [
    r"zentral\w*\s*/\s*dezentral\w*", r"\bKonzern\w*", r"\bTochtergesellschaft\w*", r"\bLandesgesellschaft\w*",
    r"\bmehrere\s+Standorte\b", r"\bHolding\b", r"\bVerbund\b", r"\bMuttergesellschaft\b",
]
STRUCTURE_RE = re.compile("|".join(STRUCTURE_HINTS), re.I)

# Case-sensitive proper nouns. Names that are also ordinary words require a legal-form suffix.
LEGAL = r"(?=\s+(?:GmbH|AG|SE|S\.p\.A\.|Ltd|Inc|KG|Group|Deutschland))"
BROKER_RE = re.compile(
    r"\b(Experis|Hays(?: Technology)?|GULP|Gulp|Randstad Professional|Westhouse|Solcom|SOLCOM|Projekt Broker|"
    r"Krongaard|KRONGAARD|Computer Futures|SThree|Etengo|top itservices|Ratbacher|Michael Page|"
    r"Robert Half|Tenth Revolution(?: Group)?|FRG Technology|Nigel Frank|Harvey Nash|"
    r"Reply" + LEGAL + r"|Amoria Bond|Darwin Recruitment|Modis" + LEGAL + r"|Akkodis|Allgeier|Ferchau|FERCHAU|"
    r"Brunel" + LEGAL + r"|Computacenter|Synergie-Effekt|mund consulting|Aleri|Effection)\b")
# Contact: optional colon, optional salutation and title, 1 to 3 capitalised words on the same line.
CONTACT_RE = re.compile(
    r"(?:Ansprechpartner(?:in)?|Ihr(?:e)? Ansprechpartner(?:in)?|Kontakt(?:person)?)\s*:?[ \t]*"
    r"(?:(?:Frau|Herr|Hr\.|Fr\.|Ms\.?|Mr\.?)[ \t]+)?(?:(?:Dr\.|Prof\.)[ \t]+)?"
    r"([A-ZÄÖÜ][\w\-]+(?:[ \t]+[A-ZÄÖÜ][\w\-]+){0,2})")
# "Essen" is left out: as a word it is more often food than the city.
CITY_RE = re.compile(
    r"\b(Frankfurt(?: am Main)?|Berlin|Hamburg|München|Köln|Düsseldorf|Stuttgart|"
    r"Hannover|Nürnberg|Leipzig|Bremen|Dortmund|Bonn|Mainz|Wiesbaden|"
    r"Karlsruhe|Mannheim|Darmstadt|Bad Homburg|Eschborn|Zürich|Wien|Bern)\b")


# --- helpers -----------------------------------------------------------------

def first(pattern, text, group=0):
    m = pattern.search(text)
    return m.group(group) if m else None


def to_int(value):
    return int(value) if value else None


def first_group(pattern, text):
    """First match's first non-empty capture group."""
    m = pattern.search(text)
    if not m:
        return None
    return next((g for g in m.groups() if g), None)


def best_date(pattern, text):
    """Prefer a full date (dd.mm.yyyy or ISO) over a month (mm/yyyy) among all matches."""
    hits = [h for h in pattern.findall(text) if h]
    if not hits:
        return None
    full = [h for h in hits if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}|\d{4}-\d{2}-\d{2}", h)]
    return full[0] if full else hits[0]


def uniq(seq):
    """Dedupe case-insensitively and return the canonical spelling where one is known."""
    seen, out = set(), []
    for s in seq:
        if not s:
            continue
        k = s.lower().replace(" ", "")
        if k not in seen:
            seen.add(k)
            out.append(CANON.get(k, s))
    return out


def normalise(text: str) -> str:
    """NFKC, lowercase, NBSP and wrapping removed, punctuation stripped, broker and contact lines dropped."""
    text = unicodedata.normalize("NFKC", text)
    lines = []
    for line in text.splitlines():
        if BROKER_RE.search(line) or CONTACT_RE.search(line):
            continue
        lines.append(line)
    joined = " ".join(lines).lower()
    joined = re.sub(r"[^\w\s§%/+-]", " ", joined)
    return re.sub(r"\s+", " ", joined).strip()


def fingerprint(text: str) -> str:
    return hashlib.sha1(normalise(text).encode("utf-8")).hexdigest()[:12]


def near_key(text: str, k: int = 5, positions: int = 32) -> str:
    """MinHash signature over k-word shingles; hex, two characters per position."""
    words = normalise(text).split()
    if len(words) < k:
        return ""
    shingles = {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}
    out = []
    for p in range(positions):
        salt = str(p).encode()
        best = min(hashlib.blake2b(salt + s.encode("utf-8"), digest_size=4).digest() for s in shingles)
        out.append(f"{best[0]:02x}")
    return "".join(out)


def near_similarity(a: str, b: str) -> float:
    """Share of equal positions in two near_keys, 0..1."""
    if not a or not b or len(a) != len(b):
        return 0.0
    pairs = [(a[i:i + 2], b[i:i + 2]) for i in range(0, len(a), 2)]
    return sum(1 for x, y in pairs if x == y) / len(pairs)


# --- parse -------------------------------------------------------------------

def parse(text: str) -> dict:
    dates = [f"{d}.{m}.{y}" for d, m, y in DATE_RE.findall(text)]
    months = [f"{m}/{y}" for m, y in MONTH_RE.findall(text)]
    constraints = {k: bool(re.search(v, text, re.I)) for k, v in CONSTRAINTS.items()}

    remote = REMOTE_RE.search(text)
    remote_pct = to_int(remote.group(1) or remote.group(2)) if remote else None
    sector = first(SECTOR_RE, text, 1)

    return {
        "broker": first(BROKER_RE, text),
        "contact": first(CONTACT_RE, text, 1),
        "posted_at": first(POSTED_RE, text, 1),
        "sector_line": sector.strip() if sector else None,
        "start": best_date(START_RE, text) or (months[0] if months else None),
        "end": best_date(END_RE, text),
        "dates_mentioned": uniq(dates),
        "duration_months": to_int(first_group(DURATION_RE, text)),
        "person_days": to_int(first(PT_RE, text, 1)),
        "remote_share_pct": remote_pct,
        "cities": uniq(CITY_RE.findall(text)),
        "certifications": uniq(CERT_RE.findall(text)),
        "framework_terms": uniq(FRAMEWORK_RE_CI.findall(text) + FRAMEWORK_RE_CS.findall(text)),
        "structure_hints": uniq(STRUCTURE_RE.findall(text)),
        "constraints": constraints,
        "word_count": len(text.split()),
        "fingerprint": fingerprint(text),
        "near_key": near_key(text),
    }


# --- input -------------------------------------------------------------------

def read_text(path: Path) -> tuple[str, dict]:
    """Return (text, meta). .eml files yield headers and the text/plain body."""
    raw = path.read_bytes()
    meta = {}
    if path.suffix.lower() == ".eml":
        msg = BytesParser(policy=policy.default).parsebytes(raw)
        meta = {"from": msg.get("From"), "date": msg.get("Date"), "subject": msg.get("Subject")}
        body = msg.get_body(preferencelist=("plain", "html"))
        text = body.get_content() if body else ""
        if body is not None and body.get_content_type() == "text/html":
            text = re.sub(r"<[^>]+>", " ", text)
        return text, meta
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("cp1252", errors="replace")
        meta["encoding"] = "cp1252 (utf-8 failed)"
    if "�" in text:
        print("warning: replacement characters in input; umlauts and the fingerprint may be off", file=sys.stderr)
    return text, meta


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="posting as .txt/.md, or an alert mail as .eml")
    ap.add_argument("-o", "--out")
    args = ap.parse_args()
    text, meta = read_text(Path(args.file))
    result = parse(text)
    if meta:
        result["mail"] = meta
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload + "\n")


if __name__ == "__main__":
    main()
