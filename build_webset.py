"""
Build an Exa Webset of voice AI agent startups (vertical, not infra) that
raised pre-seed -> Series B in the last 2 years, then enrich each with the
lead VC firm + the partner who led the round.
"""
import os
import json
import sys
import time

from exa_py import Exa
from exa_py.websets.types import (
    CreateWebsetParameters,
    CreateEnrichmentParameters,
)

API_KEY = os.environ["EXA_API_KEY"]
exa = Exa(API_KEY)

QUERY = (
    "Voice AI agent startups building vertical voice agents (e.g. for "
    "healthcare, sales, recruiting, customer support, restaurants, "
    "debt collection, legal, real estate, insurance, logistics) that "
    "raised pre-seed, seed, Series A, or Series B funding between "
    "April 2024 and April 2026. Exclude pure voice infrastructure, "
    "TTS/STT model providers, and low-level voice APIs."
)

CRITERIA = [
    {"description": "Company builds voice AI agents for a specific vertical/application, not general voice infrastructure, TTS/STT models, or low-level voice APIs."},
    {"description": "Company raised a pre-seed, seed, Series A, or Series B round between April 2024 and April 2026."},
    {"description": "Round was announced publicly in TechCrunch, Forbes, Axios Pro, Business Insider, press release, or the firm's website."},
]

ENRICHMENTS = [
    CreateEnrichmentParameters(
        description="Name of the lead venture capital firm on the most recent pre-seed / seed / Series A / Series B round.",
        format="text",
    ),
    CreateEnrichmentParameters(
        description="All venture capital firms that participated in the most recent pre-seed / seed / Series A / Series B round (comma separated).",
        format="text",
    ),
    CreateEnrichmentParameters(
        description="Full name of the partner at the lead VC firm who led the round and typically took a board seat or observer seat.",
        format="text",
    ),
    CreateEnrichmentParameters(
        description="Funding stage of the most recent round (pre-seed, seed, Series A, or Series B).",
        format="options",
        options=[
            {"label": "pre-seed"},
            {"label": "seed"},
            {"label": "Series A"},
            {"label": "Series B"},
        ],
    ),
    CreateEnrichmentParameters(
        description="Announcement date of the most recent round (YYYY-MM-DD).",
        format="date",
    ),
    CreateEnrichmentParameters(
        description="Round size in USD millions for the most recent round.",
        format="number",
    ),
    CreateEnrichmentParameters(
        description="Vertical / use case the voice AI agent targets (one short phrase).",
        format="text",
    ),
]


def main() -> None:
    print("Creating webset...", flush=True)
    webset = exa.websets.create(
        params=CreateWebsetParameters(
            search={
                "query": QUERY,
                "count": 80,
                "criteria": CRITERIA,
                "entity": {"type": "company"},
            },
            enrichments=ENRICHMENTS,
            metadata={"project": "voice-ai-vc-map"},
        )
    )
    print(f"Webset ID: {webset.id}", flush=True)
    print(f"Dashboard: {getattr(webset, 'dashboard_url', 'n/a')}", flush=True)

    with open("/home/user/aidanhchau/webset_id.txt", "w") as f:
        f.write(webset.id + "\n")

    print("Waiting until idle (this can take several minutes)...", flush=True)
    start = time.time()
    idle = exa.websets.wait_until_idle(webset.id, timeout=3600, poll_interval=15)
    print(f"Idle after {int(time.time() - start)}s. Status: {idle.status}", flush=True)


if __name__ == "__main__":
    main()
