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
    frequency_growth_time: Dict[int, int] = {}


@app.get("/allBerryStats", response_model=AllBerryStatsResponse)
async def get_all_berry_stats():
    return AllBerryStatsResponse()
