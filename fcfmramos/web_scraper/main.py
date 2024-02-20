import asyncio

from fcfmramos.web_scraper.client import Client

# from cache import HashCache
from fcfmramos.web_scraper.scraper import scrape_catalogo
from fcfmramos.web_scraper.ucampus import Departamento


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
    20161
]
DEPARTMENTS = [
    Departamento(5, "Departamento de Ciencias de la Computación", "CC", "FFFFFF"),
]


async def main():
    client = Client()
    # TODO: all of this
    # tasks = []

    # page_cache = HashCache("pages")
    # print(page_cache.has("Hi!"))
    # page_cache.add("Hi!")
    # page_cache.save()

    catalogos = []

    for semester in SEMESTERS:
        for department in DEPARTMENTS:
            catalogos.append(await scrape_catalogo(client, semester, department))

    return catalogos


if __name__ == "__main__":
    asyncio.run(main())
