from functools import lru_cache
from statistics import mean, median, variance
from collections import Counter
from fastapi import FastAPI
from requests import get
from pydantic import BaseModel
from typing import List, Dict
from os import getenv
from dotenv import load_dotenv

# load env vars
load_dotenv()


app = FastAPI(title="Poke Berries Statistics")


class AllBerryStatsResponse(BaseModel):
    berries_names: List[str] = []
    min_growth_time: int = 0
    median_growth_time: float = 0
    max_growth_time: int = 0
    variance_growth_time: float = 0
    mean_growth_time: float = 0
    frequency_growth_time: Dict[int, int]


def get_berry_growth_time(berry_info_url: str) -> int:
    berry_info = get(berry_info_url).json()
    return berry_info.get("growth_time")


def get_berries(berries_url: str) -> dict:
    berries_response = get(berries_url).json()
    return berries_response


if getenv("CACHE") == "TRUE":
    get_berry_growth_time = lru_cache(get_berry_growth_time)
    get_berries = lru_cache(get_berries)


@app.get("/allBerryStats", response_model=AllBerryStatsResponse)
async def get_all_berry_stats():
    berries_names = []
    berries_growth_times = []
    berries_url = getenv("BERRIES_URL")
    while berries_url:
        response = get_berries(berries_url)
        for berry in response.get("results"):
            berries_names.append(berry.get("name"))
            berry_growth_time = get_berry_growth_time(berry.get("url"))
            berries_growth_times.append(berry_growth_time)
        berries_url = response.get("next")

    berry_stats = {
        "berries_names": berries_names,
        "min_growth_time": min(berries_growth_times),
        "median_growth_time": median(berries_growth_times),
        "max_growth_time": max(berries_growth_times),
        "variance_growth_time": variance(berries_growth_times),
        "mean_growth_time": mean(berries_growth_times),
        "frequency_growth_time": Counter(berries_growth_times),
    }
    return berry_stats
