# CHC Technology SEO

**A bilingual Vietnamese–English SEO toolkit for Claude Code.** Audit websites, explain evidence, and build prioritized fixes for Vietnam and international markets.

[Tiếng Việt](README.md) · [Skill guide](skills/chc-seo/SKILL.md) · [API inventory](API-INVENTORY.md) · [Notices and licenses](THIRD-PARTY-NOTICES.md)

> **Install the full repository as a GitHub plugin.** It contains over 500 files; Claude's **Upload a skill** flow has a 200-file limit and rejects nested ZIP files.

## Install with Claude Code

Run these commands inside Claude Code:

```text
/plugin marketplace add chctechjsc-code/chc-technology-seo
/plugin install chc-technology-seo@chc-technology-seo
/chc-technology-seo:chc-seo setup
```

`setup` creates a dedicated Python environment and installs the required libraries. Check it with `/chc-technology-seo:chc-seo doctor`. Browser-based checks also need Chromium to finish installing.

### Windows: clone and install

```powershell
git clone --depth 1 https://github.com/chctechjsc-code/chc-technology-seo.git
powershell -ExecutionPolicy Bypass -File .\chc-technology-seo\install.ps1
```

Review `install.ps1` before running it. The script validates the plugin, installs it from the clone, and sets up the Python runtime. Use `-ValidateOnly` to inspect without installing, or `-SkipSetup` if the runtime is already prepared. On macOS/Linux, use the three Claude Code commands above; this repository does not yet ship a separate shell installer.

## First commands

```text
/chc-technology-seo:chc-seo audit https://example.com lang=en
/chc-technology-seo:chc-seo page https://example.com/product lang=vi
/chc-technology-seo:chc-seo hreflang https://example.com lang=both
/chc-technology-seo:chc-seo schema https://example.com
```

The skill responds in Vietnamese or English. `lang=both` requests two equivalent report sections. Report language and target market are separate choices. The URLs above only illustrate syntax.

## What is included

| Area | Coverage |
|---|---|
| Audits | Site and page audits, technical SEO, sitemaps, images, performance, and change tracking |
| Content | Quality, E-E-A-T, briefs, keyword clusters, comparison pages, and search experience |
| Emerging search | GEO, AI agent access, and structured data |
| Markets | Local SEO, maps, ecommerce, hreflang, and international SEO |
| Data | Google, backlinks, and optional providers after valid account configuration |

The repository includes **one CHC routing skill** with 25 bilingual modes, 26 detailed technical guides, 19 specialist agents, and more than 60 scripts. Nine extension directories contain optional integration code; bundling that code does not activate any provider.

SEO findings should name the URL and sample scope, retrieval time, evidence, confidence, and a way to verify a fix. When a metric cannot be measured, report “Not measured” instead of inventing a value.

## APIs and data access

- **Public starting points:** HTML, robots.txt, sitemaps, and checks that need no account once the relevant runtime is ready.
- **Site or account authorization:** Search Console, Analytics, Bing Webmaster, and similar sources require valid access.
- **Optional vendors:** Ahrefs, DataForSEO, SE Ranking, Profound, and others may require separate contracts, API keys, or charges. No provider keys are bundled.

Read the [API inventory](API-INVENTORY.md) before connecting a service. An integration that has not been configured and tested with an authorized account should not be described as operational.

## Repository layout

```text
.claude-plugin/                 plugin and marketplace manifests
skills/chc-seo/SKILL.md        single CHC entry point
skills/chc-seo/references/     Vietnamese and English guides
skills/chc-seo/skills/         detailed technical procedures
skills/chc-seo/scripts/        runtime and checks
skills/chc-seo/extensions/     optional integration source
agents/                        19 Claude Code agents
install.ps1                    Windows installer
```

Validate the repository before use or contribution:

```powershell
claude plugin validate .
powershell -ExecutionPolicy Bypass -File .\install.ps1 -ValidateOnly
python .\skills\chc-seo\scripts\runtime.py doctor --json
```

## Current limits

The plugin structure, document links, and Python syntax have been checked. End-to-end browser checks and vendor APIs still depend on the environment and valid access. The plugin does not guarantee rankings, traffic, or business outcomes. Claude Code and external services have their own terms.

## Provenance and license

This CHC edition adapts the workflow for Vietnamese and English use and is distributed from this repository. Third-party source and documentation are recorded in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md), [LICENSE](LICENSE), and the bundled license files. Keep those notices when redistributing the project.
