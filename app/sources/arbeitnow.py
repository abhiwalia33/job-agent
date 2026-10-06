# app/sources/arbeitnow.py
from datetime import datetime, timezone

import requests

from app.schemas.job import JobPosting

URL = "https://www.arbeitnow.com/api/job-board-api"


def fetch_arbeitnow() -> list[JobPosting]:
    # 1. fetch
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    items = response.json()["data"]

    # 2. loop and convert
    postings = []
    for item in items:
        posting = JobPosting(
            source="arbeitnow",
            source_id=item["slug"],
            title=item["title"],
            company=item["company_name"],
            location=item.get("location"),
            url=item["url"],
            description=item["description"],
            posted_at=datetime.fromtimestamp(item["created_at"], tz=timezone.utc),
        )
        postings.append(posting)
    return postings


def search_arbeitnow(query: str, limit: int = 10) -> list[JobPosting]:
    query = query.lower()
    matches = []
    for posting in fetch_arbeitnow():
        text = posting.title.lower()
        if query in text:
            matches.append(posting)
    return matches[:limit]


if __name__ == "__main__":
    for p in search_arbeitnow("data")[:3]:
        print(p.title, "|", p.company)