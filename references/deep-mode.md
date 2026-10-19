# Deep mode (optional, expensive)

Standard mode runs the mirror search, the procurement-signature check and the feedback loop in about 30 tool calls. Deep mode adds the steps below and typically costs three to five times as many searches and far more context. Run it only when the user asks for it explicitly ("deep", "gründlich", "alles") after you have said what it costs, or when a standard run ends at medium confidence and the user wants certainty.

## Temporal correlation
Search the four weeks before the posting date for the candidate's own job ads (security roles, vacancies in leadership), tender notices (TED, national portals), press on executive changes, incidents or regulatory findings. Each hit is dated and goes into "Verified".

## Falsification
For the top candidate, search for the organisations that would also fit the same clues. If one exists, the candidate drops from verified to inferred and the report shows both. Only when the search for alternatives comes back empty may the report say "verified".

## Register sources
Managing directors, subsidiaries and group structure: the official registers (Handelsregister, Bundesanzeiger) block automated fetching, so use the search snippets of register aggregators (northdata.de, offeneregister.de, companyhouse) or ask the user to look the entry up and paste it. Role holders: association and member lists (BDEW, VDE, ISACA, UP KRITIS) and conference programmes. Slower than aggregator sites, but authoritative and dated.

## Case file
Write the case as JSON to `cases/<fingerprint>.json` in the profile folder: parsed posting, mirrors with URLs, candidates with evidence for and against, and the people layer as role, organisation, source and source date only, no derived email addresses and no contact details. The file exists so a follow-up question does not repeat the research. It is personal data under SECURITY.md section 4: when a case is closed (outcome recorded, or no contact made within the approach), remind the user to delete it; on a later run that finds a case file older than 90 days, say so and offer to delete it. On a surface with no persistent folder, skip the case file.

## Candidate fan-out
With a subagent tool available, give each candidate to its own subagent with a fixed budget (10 searches) and a fixed output shape (evidence for, evidence against, people with sources and dates). Pass the posting text and the candidate name; never pass the user's profile. The coordinator merges. Faster and keeps the main context clean, at the price of parallel token use.

## Query library
Run the full set of query templates per stage rather than stopping at the first hits: distinctive phrases, numbers, platform-scoped variants, German and English wording, broker listing pages. Expect diminishing returns after the fifth variant per anchor.

## Saying what it costs
Before starting deep mode, tell the user in one line: roughly how many searches, that results will be more certain but not guaranteed, and that they can stop after any stage.
