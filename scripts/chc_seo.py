#!/usr/bin/env python3
"""CHC Technology SEO public-web checks, without vendor credentials."""
from __future__ import annotations

import argparse
import html.parser
import http.client
import ipaddress
import json
import socket
import ssl
import urllib.error
import urllib.parse
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

USER_AGENT = "CHC-SEO/1.0 (+public website audit)"
LIMIT = 2_000_000


def resolve_public_url(raw: str):
    if re.search(r"[\x00-\x20\x7f]", raw):
        raise ValueError("URL contains control characters or whitespace")
    parts = urllib.parse.urlsplit(raw)
    if parts.scheme not in ("http", "https") or not parts.hostname or parts.username or parts.password:
        raise ValueError("Only public http(s) URLs without credentials are allowed")
    host = parts.hostname.encode("idna").decode("ascii")
    port = parts.port or (443 if parts.scheme == "https" else 80)
    addresses = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    if not addresses:
        raise ValueError("Hostname has no address")
    for item in addresses:
        address = ipaddress.ip_address(item[4][0])
        if not address.is_global:
            raise ValueError("Private, loopback and reserved addresses are blocked")
    return parts, host, port, addresses[0][4][0]


def safe_url(raw: str) -> str:
    resolve_public_url(raw)
    return raw


def fetch(url: str) -> dict:
    current = url
    for hop in range(4):
        parts, host, port, address = resolve_public_url(current)
        # Connect to the validated IP. This prevents a second DNS lookup from
        # switching the request to an internal address after validation.
        conn = http.client.HTTPConnection(host, port, timeout=15)
        raw_sock = socket.create_connection((address, port), timeout=15)
        try:
            if parts.scheme == "https":
                try:
                    conn.sock = ssl.create_default_context().wrap_socket(raw_sock, server_hostname=host)
                except Exception:
                    raw_sock.close()
                    raise
            else:
                conn.sock = raw_sock
            target = urllib.parse.urlunsplit(("", "", parts.path or "/", parts.query, ""))
            conn.putrequest("GET", target, skip_host=True)
            conn.putheader("Host", parts.netloc)
            conn.putheader("User-Agent", USER_AGENT)
            conn.putheader("Accept", "text/html,application/xml,text/plain;q=0.8")
            conn.endheaders()
            response = conn.getresponse()
            if response.status in (301, 302, 303, 307, 308):
                location = response.getheader("Location")
                if not location:
                    raise ValueError("Redirect lacks Location header")
                if hop == 3:
                    raise ValueError("More than three redirects")
                current = urllib.parse.urljoin(current, location)
                continue
            data = response.read(LIMIT + 1)
            if len(data) > LIMIT:
                raise ValueError("Response exceeds 2 MB limit")
            charset = response.headers.get_content_charset() or "utf-8"
            return {"url": current, "status": response.status,
                    "content_type": response.getheader("Content-Type", ""),
                    "text": data.decode(charset, "replace")}
        finally:
            conn.close()
    raise ValueError("Redirect limit exceeded")


class PageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.h1 = []
        self.meta = {}
        self.links = []
        self.images = []
        self.lang = None
        self._capture = None
        self._buffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag in ("title", "h1"):
            self._capture, self._buffer = tag, []
        if tag == "meta" and a.get("name"):
            self.meta[a["name"].lower()] = a.get("content", "")
        if tag == "link":
            self.links.append(a)
        if tag == "img":
            self.images.append({"src": a.get("src"), "alt": a.get("alt")})

    def handle_data(self, data):
        if self._capture:
            self._buffer.append(data)

    def handle_endtag(self, tag):
        if tag == self._capture:
            value = " ".join(" ".join(self._buffer).split())
            if tag == "title":
                self.title = value
            elif value:
                self.h1.append(value)
            self._capture, self._buffer = None, []


def robots_url(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, "/robots.txt", "", ""))


def inspect(url: str, mode: str) -> dict:
    page = fetch(url)
    result = {"brand": "CHC Technology", "mode": mode, "requested_url": url, "fetched_at": datetime.now(timezone.utc).isoformat(), "page": {k: v for k, v in page.items() if k != "text"}, "findings": [], "limitations": ["Static HTML only; JavaScript rendering, indexing status and Core Web Vitals were not measured"]}
    findings = result["findings"]

    def add(code, priority, evidence, action):
        findings.append({"id": code, "priority": priority, "evidence": evidence, "recommendation": action})

    if page["status"] != 200:
        add("HTTP_STATUS", "P0" if page["status"] >= 400 else "P1", f"HTTP {page['status']}", "Investigate the response for the intended canonical page")
    if "html" in page["content_type"].lower():
        parsed = PageParser()
        parsed.feed(page["text"])
        canonical = [urllib.parse.urljoin(page["url"], l.get("href", "")) for l in parsed.links if l.get("rel", "").lower() == "canonical"]
        alternates = [{"hreflang": l.get("hreflang"), "href": urllib.parse.urljoin(page["url"], l.get("href", ""))} for l in parsed.links if l.get("hreflang")]
        result["html"] = {"title": parsed.title, "description": parsed.meta.get("description"), "robots": parsed.meta.get("robots"), "lang": parsed.lang, "h1": parsed.h1, "canonical": canonical, "hreflang": alternates, "image_count": len(parsed.images), "images_without_alt": [i["src"] for i in parsed.images if i["alt"] is None]}
        if not parsed.title:
            add("TITLE_MISSING", "P1", "No HTML title", "Add a descriptive, unique title")
        if not parsed.h1:
            add("H1_MISSING", "P2", "No H1 in static HTML", "Check rendered HTML and provide a clear page heading")
        if not parsed.lang:
            add("LANG_MISSING", "P2", "No html lang attribute", "Set the primary content language")
        if "noindex" in (parsed.meta.get("robots") or "").lower():
            add("NOINDEX", "P0", "Meta robots contains noindex", "Verify whether exclusion is intentional")
        if parsed.images and any(i["alt"] is None for i in parsed.images):
            add("ALT_MISSING", "P2", f"{len(result['html']['images_without_alt'])} images lack an alt attribute", "Add contextual alt or empty alt for decorative images")
    if mode == "audit":
        robots = fetch(robots_url(page["url"]))
        result["robots"] = {"url": robots["url"], "status": robots["status"], "sitemaps": [line.split(":", 1)[1].strip() for line in robots["text"].splitlines() if line.lower().startswith("sitemap:")]}
        sitemap_urls = result["robots"]["sitemaps"] or [urllib.parse.urljoin(page["url"], "/sitemap.xml")]
        result["sitemaps"] = []
        for sm_url in sitemap_urls[:3]:
            try:
                sm = fetch(sm_url)
                entry = {"url": sm["url"], "status": sm["status"]}
                if sm["status"] == 200:
                    root = ET.fromstring(sm["text"])
                    entry["root"] = root.tag.split("}")[-1]
                    entry["entry_count"] = sum(1 for child in root if child.tag.split("}")[-1] in ("url", "sitemap"))
                result["sitemaps"].append(entry)
            except (ValueError, ET.ParseError, urllib.error.URLError) as error:
                result["sitemaps"].append({"url": sm_url, "error": str(error)})
        result["limitations"].append("This audit checks one page plus robots.txt and up to three sitemap files; it is not a full crawl")
    return result


def main():
    parser = argparse.ArgumentParser(description="CHC SEO public website inspection")
    parser.add_argument("mode", choices=("page", "audit"))
    parser.add_argument("url")
    parser.add_argument("--lang", choices=("vi", "en"), default="vi", help="Report prose language is handled by the skill; JSON keys remain stable")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.url, args.mode), ensure_ascii=False, indent=2))
    except (ValueError, urllib.error.URLError, TimeoutError, OSError) as error:
        parser.exit(2, f"CHC SEO: {error}\n")


if __name__ == "__main__":
    main()
