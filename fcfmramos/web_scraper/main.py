import asyncio
from pathlib import Path

from fcfmramos.web_scraper.client import Client, load_cookies

# from cache import HashCache
from fcfmramos.web_scraper.catalogo_scraper import scrape_catalogo
from fcfmramos.web_scraper.plan_scraper import scrape_plan
from fcfmramos.web_scraper.ucampus import Departamento, Plan


SEMESTERS = [
    20232,
    20231,
    20222,
    20221,
    20212,
    20211,
    20202,
    20201,
    20192,
    20191,
    20182,
    20181,
    20172,
    20171,
    20162,
    20161,
]
DEPARTMENTS = [
    Departamento(
        5, "Departamento de Ciencias de la Computación", "CC", "FFFFFF"
    ),
]
PLANS = [
    Plan(
        41, 5, "", [], 5
    )
]


async def scrape_catalogos():
    current_dir = Path(__file__).parent
    ucampus_client = Client(load_cookies(current_dir / "ucampus.cookie"))
    ucursos_client = Client(load_cookies(current_dir / "ucursos.cookie"))

    catalogos = []

    for semester in SEMESTERS:
        for department in DEPARTMENTS:
            print(f"Scraping {semester} {department.nombre}")
            catalogos.append(
                await scrape_catalogo(
                    ucampus_client, ucursos_client, semester, department
                )
            )

    return catalogos


async def scrape_planes():
    current_dir = Path(__file__).parent
    # cache_path = current_dir / "planes_cache.pkl"  # Define cache file path

    # # Check if cache exists and is not empty
    # if cache_path.exists() and cache_path.stat().st_size > 0:
    #     with open(cache_path, "rb") as cache_file:
    #         try:
    #             planes = pickle.load(cache_file)
    #             print("Loaded data from cache.")
    #             return planes
    #         except (pickle.PickleError, EOFError):
    #             print("Cache file is corrupted or unreadable, scraping again.")

    # If cache does not exist or is corrupted, proceed with scraping
    ucampus_client = Client(load_cookies(current_dir / "ucampus.cookie"))
    planes = []
    for plan in PLANS:
        planes.append(
            await scrape_plan(ucampus_client, plan)
        )

    # # Cache the result
    # with open(cache_path, "wb") as cache_file:
    #     pickle.dump(planes, cache_file)
    #     print("Cached scraped data.")

    return planes


if __name__ == "__main__":
    print(asyncio.run(scrape_planes()))
