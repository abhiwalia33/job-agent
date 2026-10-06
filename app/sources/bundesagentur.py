# app/sources/bundesagentur.py
from datetime import datetime, timezone

import requests

from app.schemas.job import JobPosting

URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs"
HEADERS = {"X-API-Key": "jobboerse-jobsuche"}
JOB_PAGE = "https://www.arbeitsagentur.de/jobsuche/jobdetail/"


def search_bundesagentur(query: str, location: str = "Berlin", limit: int = 10) -> list[JobPosting]:
    response = requests.get(
        URL,
        headers=HEADERS,
        params={"was": query, "wo": location, "size": limit},
        timeout=10,
    )
    response.raise_for_status()
    items = response.json().get("ergebnisliste", [])

    postings = []
    for item in items:
        ref = item["referenznummer"]
        posting = JobPosting(
            source="bundesagentur",
            source_id=ref,
            title=item["stellenangebotsTitel"],
            company=item["firma"],
            location=item["stellenlokationen"][0]["adresse"]["ort"],
            url=JOB_PAGE + ref,
            posted_at=datetime.fromisoformat(
                item["datumErsteVeroeffentlichung"]
            ).replace(tzinfo=timezone.utc),
        )
        postings.append(posting)
    return postings


if __name__ == "__main__":
    for p in search_bundesagentur("Data Scientist")[:3]:
        print(p.title, "|", p.company, "|", p.location)