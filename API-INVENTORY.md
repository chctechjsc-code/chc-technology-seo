# CHC Technology — API inventory (2026-10-29)

“Public” means accessible without a private account credential, subject to provider terms and rate limits. It does not mean unlimited or unrestricted commercial use.

| Capability | Status | CHC decision |
|---|---|---|
| Public website HTML, robots.txt, XML sitemap | Public web | One-shot checks are implemented in `skills/chc-seo/scripts/chc_seo.py`. The CLI is not a crawler and does not enforce a crawl schedule; the caller must respect site policy and rate limits. |
| PageSpeed Insights v5 | Public endpoint, optional Google API key for repeated use | Eligible for a future CHC adapter; not wired into default CLI. Do not rely on PSI for CrUX field data after announced change. |
| Common Crawl index | Public data / query service | Eligible for a future CHC adapter with query limits; not a complete backlink database. |
| Google Search Console, URL Inspection, GA4, Google Ads | Authenticated property/account data | CHC-owned OAuth client and user authorization required. No upstream credentials or configuration. |
| CrUX API | Google project key required | Build CHC adapter after project setup; PSI substitute is not equivalent. |
| Bing Webmaster / IndexNow | Site access or submission credentials as applicable | Build CHC adapter with CHC/user-owned verification and keys. |
| Google Business Profile / Maps Platform | Account, project or billable API access | Separate CHC adapter when authorized and budgeted. |
| DataForSEO, Ahrefs, Moz, Firecrawl, Profound, SE Ranking, Keywords Everywhere, Gemini image providers | Vendor account/API or paid service | No default execution; design CHC adapters or replace with public methods where feasible. Do not claim identical data from public sources. |
| Matomo | Private analytics server/token | CHC adapter per client instance and consent. |

Optional extension source is included under `skills/chc-seo/extensions/`. It is not installed or connected merely by uploading the skill; provider access is still required. API names and capabilities can change; verify official docs before implementation.

Official references: [Google Search Console authorization](https://developers.google.com/webmaster-tools/v1/how-tos/authorizing), [PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started), [Common Crawl Index](https://index.commoncrawl.org/).
