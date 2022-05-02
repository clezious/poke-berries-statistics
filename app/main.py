from functools import lru_cache
from statistics import mean, median, variance
from collections import Counter
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from requests import get
from pydantic import BaseModel
from typing import List, Dict
from os import getenv
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import base64
from io import BytesIO

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
    """Performs a GET Request to the received berry_info_url and returns the growth_time of the response body"""
    berry_info = get(berry_info_url).json()
    return berry_info.get("growth_time")


def get_berries(berries_url: str) -> dict:
    """Performs a GET Request to the received berries_url and returns the response body parsed as a dict"""
    berries_response = get(berries_url).json()
    return berries_response


# If specified by environment variable "CACHE", performs simple caching using functools.lru_cache
# This allows subsequent api calls to be faster, at the expense of increased memory usage and
# (since no cache invalidation techniques are implemented) not being able to see future data updates.
if getenv("CACHE") == "TRUE":
    get_berry_growth_time = lru_cache(get_berry_growth_time)
    get_berries = lru_cache(get_berries)


@app.get("/graph", response_class=HTMLResponse)
async def graph():
    """Returns a Histogram of the frequency of growth times of all berries in HTML"""
    stats = await get_all_berry_stats()
    berries_growth_times = [
        int(key)
        for key, val in stats.get("frequency_growth_time").items()
        for x in range(val)
    ]
    # Generate histogram of growth time frequencies
    fig = plt.figure()
    plt.xlabel("Growth Time (s)")
    plt.ylabel("Frequency")
    plt.hist(berries_growth_times, bins=max(stats.get("frequency_growth_time").keys()))

    # Save plot into base64 encoded img
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format="png")
    encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")

    html_content = f"""
        <html>
            <head>
                <title>Growth time frequency histogram</title>
            </head>
            <body>
                <h1>Growth time frequency histogram</h1>
                <img src=\'data:image/png;base64,{encoded}\'>
            </body>
        </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/allBerryStats", response_model=AllBerryStatsResponse)
async def get_all_berry_stats():
    """To get a series of statistics on Poke-Berries"""
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
