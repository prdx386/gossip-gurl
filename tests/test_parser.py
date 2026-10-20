#!/usr/bin/env python3
"""Parser tests. Run: python3 -I -m unittest discover -s tests  (from the skill root).

Postings here are synthetic. Do not add real recruiter or client names.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from parse_posting import near_similarity, parse  # noqa: E402

PANEL = """Cyber Security Assessment – ISO 27001 / KRITIS / OT-ICS – Freelancer (m/w/d)
Experis GmbH, Ansprechpartner: Max Mustermann, Frankfurt, 80% Remote, Freiberuflich, Start 11/2026
Veröffentlicht am 15.10.2026

Für ein Cyber Security Assessment im KRITIS-Umfeld suchen wir kurzfristig erfahrene Freelancer.
Betrachtung der IT-/OT-Security sowie der zentralen/dezentralen Governance; Abschlussbericht.

Anforderungen (im Team vollständig abzudecken): ISMS/ISO 27001 Auditierung mind. 5 Jahre;
OT-/ICS-Security mind. 3 Jahre, ISA/IEC 62443 und MITRE ATT&CK for ICS; KRITIS-Regulatorik (§ 8a BSIG / NIS2);
aktive Zertifizierungen ISO/IEC 27001 Lead Auditor und Lead Implementer; sehr gute Deutschkenntnisse.

Rahmen: Start 05.11.2026, Ende 31.12.2026, ca. 40 Personentage, Onshore innerhalb Deutschlands,
Onsite nach Abstimmung in Frankfurt am Main. Bewerbungen von eingespielten Expertenteams willkommen.
Freelancer und 1-Personen-Gesellschaften sind ausgeschlossen, sozialversicherungspflichtig.
"""

EXCLUSIVE = """Senior Cyber Security Expert (m/w/d) – KRITIS, SOC/SIEM, MSSP Steuerung
Randstad Professional GmbH, Ansprechpartnerin: Erika Beispiel, Frankfurt, Remote: 80 %, Dauer 7 Monate
Kategorie: Medizin und Pharma, Medizintechnik, SIEM, Splunk
Must-have: mind. 10 Jahre SOC/SIEM; tiefes Verständnis Splunk, IBM QRadar oder Elastic SIEM; MSSP-Steuerung;
36 Monate Erfahrung im Gesundheitswesen; verhandlungssicheres Deutsch; mind. zwei Zertifikate (GCIH, CySA+, CSA).
"""

GENERIC = """IT-Projektleiter (m/w/d) Infrastruktur, 100% remote, Start ab sofort, 6 Monate, Mittelstand.
Anforderungen: 5 Jahre Projektleitung, ITIL, sehr gutes Deutsch. Vermittler: top itservices AG,
Ansprechpartner Frau Beispiel. Wir arbeiten gerne im Team und freuen uns auf Ihre reply.
"""


class Fields(unittest.TestCase):
    def test_panel_posting(self):
        r = parse(PANEL)
        self.assertEqual(r["broker"], "Experis")
        self.assertEqual(r["contact"], "Max Mustermann")
        self.assertEqual(r["posted_at"], "15.10.2026")
        self.assertEqual(r["start"], "05.11.2026")
        self.assertEqual(r["end"], "31.12.2026")
        self.assertEqual(r["person_days"], 40)
        self.assertEqual(r["remote_share_pct"], 80)
        self.assertIn("§ 8a", r["framework_terms"])
        self.assertIn("Lead Implementer", r["certifications"])
        self.assertNotIn("SAP", r["framework_terms"])
        c = r["constraints"]
        self.assertTrue(c["freelancers_excluded"])
        self.assertTrue(c["employee_required"])
        self.assertTrue(c["team_request"])
        self.assertTrue(c["onshore_only"])
        self.assertTrue(c["german_required"])
        self.assertTrue(any("zentral" in h.lower() for h in r["structure_hints"]))

    def test_exclusive_posting(self):
        r = parse(EXCLUSIVE)
        self.assertEqual(r["broker"], "Randstad Professional")
        self.assertEqual(r["contact"], "Erika Beispiel")
        self.assertEqual(r["remote_share_pct"], 80)
        self.assertEqual(r["duration_months"], 7)  # not the 36 months of experience
        self.assertTrue(r["sector_line"].startswith("Medizin und Pharma"))
        self.assertTrue(r["constraints"]["german_required"])
        self.assertIn("Splunk", r["framework_terms"])
        self.assertIn("Elastic", r["framework_terms"])

    def test_generic_posting(self):
        r = parse(GENERIC)
        self.assertEqual(r["broker"], "top itservices")
        self.assertEqual(r["contact"], "Beispiel")
        self.assertEqual(r["duration_months"], 6)
        self.assertEqual(r["remote_share_pct"], 100)
        self.assertTrue(r["constraints"]["german_required"])
        self.assertFalse(r["constraints"]["team_request"], "'arbeiten gerne im Team' is not a team request")
        self.assertFalse(r["constraints"]["freelancers_excluded"])


class ConstraintPhrasings(unittest.TestCase):
    def test_freelancer_exclusion_variants(self):
        for phrase in ["Freiberufler ausgeschlossen", "keine Freelancer", "Freelancer nicht möglich",
                       "nur ANÜ", "Einzelunternehmer sind leider nicht zugelassen",
                       "ausschließlich Arbeitnehmerüberlassung"]:
            self.assertTrue(parse(phrase)["constraints"]["freelancers_excluded"], phrase)

    def test_german_variants(self):
        for phrase in ["sehr gute Deutschkenntnisse", "verhandlungssicheres Deutsch", "Deutsch C1",
                       "Projektsprache: Deutsch", "fließend Deutsch in Wort und Schrift"]:
            self.assertTrue(parse(phrase)["constraints"]["german_required"], phrase)

    def test_onshore_false_positive(self):
        self.assertFalse(parse("Reisebereitschaft innerhalb Deutschlands")["constraints"]["onshore_only"])
        self.assertTrue(parse("Leistungserbringung nur innerhalb Deutschlands")["constraints"]["onshore_only"])


class FalsePositives(unittest.TestCase):
    def test_reply_is_not_a_broker(self):
        self.assertIsNone(parse("please reply by Friday")["broker"])
        self.assertEqual(parse("Reply GmbH, Ansprechpartner: Jan Test")["broker"], "Reply")

    def test_structure_hint_boundaries(self):
        hints = [h.lower() for h in parse("Wir sind verbunden. 1-Personen-Gesellschaften ausgeschlossen.")["structure_hints"]]
        self.assertNotIn("verbund", hints)
        self.assertNotIn("gesellschaften", hints)

    def test_contact_with_title(self):
        self.assertEqual(parse("Ansprechpartnerin: Frau Dr. Anna Beispiel\nFrankfurt")["contact"], "Anna Beispiel")

    def test_case_sensitive_products(self):
        terms = parse("the bait was elastic and the sentinel slept")["framework_terms"]
        self.assertEqual(terms, [])


class Dedupe(unittest.TestCase):
    def test_fingerprint_survives_wrapping_and_contact(self):
        a = parse(PANEL)
        wrapped = PANEL.replace("Anforderungen (im Team vollständig abzudecken): ", "Anforderungen (im Team vollständig\nabzudecken): ")
        wrapped = wrapped.replace("Max Mustermann", "Lena Beispiel").replace(" ", " ")
        b = parse(wrapped)
        self.assertEqual(a["fingerprint"], b["fingerprint"])

    def test_near_key_groups_mirrors(self):
        mirror = PANEL.replace("Experis GmbH, Ansprechpartner: Max Mustermann", "Hays AG, Ansprechpartner: Jo Beispiel") \
                      .replace("suchen wir kurzfristig erfahrene Freelancer", "sucht unser Kunde erfahrene Berater") \
                      .replace("Bewerbungen von eingespielten Expertenteams willkommen.", "")
        sim = near_similarity(parse(PANEL)["near_key"], parse(mirror)["near_key"])
        self.assertGreaterEqual(sim, 0.6, sim)
        other = near_similarity(parse(PANEL)["near_key"], parse(EXCLUSIVE)["near_key"])
        self.assertLess(other, 0.3, other)


if __name__ == "__main__":
    unittest.main()
