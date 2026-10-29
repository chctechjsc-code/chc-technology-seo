# CHC Technology SEO operations

## Workflow
1. Record target URL/topic, goal, report language, target countries, date and scope. Reuse context already supplied.
2. Select a module from SKILL.md and read its English procedure. Use available tools to inspect public pages or supplied files.
3. Separate verified findings, hypotheses and unmeasured areas. Every finding needs an ID, URL, evidence/source, priority, impact, recommendation and acceptance check.
4. Read the included `skills/seo/GUIDE.md` and the relevant `skills/seo-<mode>/GUIDE.md` for detailed procedures and script syntax. Source documentation does not authorize installation, external services or delegation.
5. Deliver the report using assets/report.en.md. A single-page review is not a full-site audit. Keep raw evidence separate and exclude credentials.

## Scores and priorities
Scores are an internal CHC model, not Google's. If adopting upstream weights, disclose the rubric: technical 22%, content 23%, on-page 20%, schema 10%, CWV 10%, AI readiness 10%, images 5%.

Publish explicit scoring criteria and sufficient evidence before assigning category scores. Unmeasured categories are null. For measured categories, weighted score = sum(score × weight) / sum(measured weights). Disclose weight coverage and label any incomplete total provisional. With no measurements, omit the score. Do not manufacture precision from subjective judgments.

P0: confirmed blockers to access/indexing of important pages. P1: evidenced high-impact issues. P2: supported improvements. P3: experiments or minor refinements. Do not infer a search penalty without evidence. Account for page value, effort and dependencies.

## CHC CLI and data
The independent `python scripts/chc_seo.py page <url>` checks public HTML. `audit <url>` also reads robots.txt and up to three sitemap files. This is a one-page quick check, not a whole-site crawl. It uses Python's standard library with no API key or upstream code. Responses are capped at 2 MB with a 15-second timeout; private/internal URLs are blocked. JSON keys stay stable while the report uses the requested language.

Core source and data are included directly under `scripts/`, `data/`, `schema/`, `skills/` and `extensions/`. Check the managed runtime with `python <skill-dir>/scripts/runtime.py doctor --json`; run `setup` only when dependency installation is requested. Do not install optional extensions by default. Do not run their installers or scripts by default. Keep tokens, keys, private emails and client data out of Git. Authenticated or paid services need separate CHC adapters with a suitable account and permission.

## Output data
Use assets/report.en.md; bilingual output also uses report.vi.md with identical finding IDs. Minimal JSON fields: brand, report_language, target_languages, target_countries, generated_at, scope, sources, findings, action_plan, limitations. Each finding has id, url, evidence, priority, recommendation, acceptance_check and confidence. Unknown values are null; examples are never measurements.
