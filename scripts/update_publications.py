#!/usr/bin/env python3
"""
Update data/publications.json for the personal webpage.

Recommended production path:
1. Add SERPAPI_KEY as a GitHub Actions repository secret.
2. Put the Google Scholar profile ID in data/profile.json.
3. Run this script from the repository root.

Google Scholar does not provide an official public API. SerpAPI is used here
because it avoids brittle page scraping from the website itself. Without a key,
the script exits cleanly and keeps the manually curated publication data.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "data" / "profile.json"
PUBLICATIONS_PATH = ROOT / "data" / "publications.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def infer_type(venue: str) -> str:
    text = venue.lower()
    if "arxiv" in text or "preprint" in text:
        return "preprint"
    if "conference" in text or "icc" in text or "globecom" in text or "workshop" in text:
        return "conference"
    return "journal"


def main() -> int:
    profile = load_json(PROFILE_PATH)
    scholar_id = profile.get("googleScholarProfileId", "").strip()
    api_key = os.environ.get("SERPAPI_KEY", "").strip()

    if not scholar_id or not api_key:
      print("Missing Google Scholar profile ID or SERPAPI_KEY; leaving publications.json unchanged.")
      return 0

    params = urllib.parse.urlencode({
        "engine": "google_scholar_author",
        "author_id": scholar_id,
        "api_key": api_key,
        "num": "100"
    })
    url = f"https://serpapi.com/search.json?{params}"

    with urllib.request.urlopen(url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    articles = payload.get("articles", [])
    publications = []
    for item in articles:
        venue = item.get("publication", "")
        link = item.get("link", "#")
        publications.append({
            "title": item.get("title", "Untitled publication"),
            "authors": item.get("authors", profile.get("name", "")),
            "venue": venue,
            "year": int(item.get("year") or 0),
            "type": infer_type(venue),
            "citations": int(item.get("cited_by", {}).get("value") or 0),
            "links": {"paper": link} if link else {}
        })

    output = {
        "updated": payload.get("search_metadata", {}).get("created_at", "recently"),
        "source": "Google Scholar author profile via SerpAPI",
        "publications": publications
    }
    PUBLICATIONS_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {len(publications)} publications.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
