import os
import pickle
from pathlib import Path

from fcfmramos.web_scraper.client import Client
from fcfmramos.web_scraper.ucampus import Plan, RamoInPlan, Subplan
from bs4 import NavigableString


def get_plan_url(plan: Plan) -> str:
    args = f"carr_codigo={plan.carr_codigo}&c_plan={plan.c_plan}"
    return (
        f"https://ucampus.uchile.cl/m/fcfm_bia/recuento_uds?{args}"
    )


async def scrape_plan(ucampus_client: Client, plan: Plan) -> Plan:
    plan_id = f"{plan.carr_codigo}_{plan.c_plan}"
    current_dir = Path(__file__).parent
    cache_path = current_dir / ".cache" / f"soup_cache_{plan_id}.pkl"
    if os.path.exists(cache_path):
        print("Using cached soup")
        with open(cache_path, "rb") as cache_file:
            soup = pickle.load(cache_file)
    else:
        url = get_plan_url(plan)
        soup = await ucampus_client.scrape(url)

        # Cache the soup for future use
        with open(cache_path, "wb") as cache_file:
            pickle.dump(soup, cache_file)

    excel_table = soup.find("table", class_="excel")
    td_colspans2 = excel_table.find_all("td", colspan="2")
    tbodies = excel_table.find_all("tbody")

    subplan_references = {}

    for i, body in enumerate(tbodies):
        title = td_colspans2[i]
        title_text = "".join(
            [
                element
                for element in title
                if isinstance(element, NavigableString)
            ]
        ).strip()
        print(title_text)

        if title_text in subplan_references:
            subplan = subplan_references[title_text]
        else:
            subplan = Subplan(title_text, [], [])
            plan.subplanes.append(subplan)

        if not plan.nombre:
            plan.nombre = title_text

        for tr in body.find_all("tr"):
            if "nodownload" in tr.get("class", []):
                lis = tr.find_all("li")
                if lis:
                    for li in lis:
                        main_text = "".join(
                            [
                                str(element).strip()
                                for element in li.contents
                                if isinstance(element, NavigableString)
                            ]
                        )
                        subplan.ramos.append(RamoInPlan(main_text))
                continue

            second_td = tr.find_all("td")[1]
            anchor = second_td.find("a")

            if anchor:
                name = anchor.text.strip()
                linked_subplan = Subplan(name, [], [])
                subplan.subplanes.append(linked_subplan)
                subplan_references[name] = linked_subplan
            else:
                name = second_td.text.strip()
                if name == "No hay ramos aprobados en esta lista.":
                    continue
                subplan.ramos.append(RamoInPlan(name))

    return plan
