from fcfmramos.web_scraper.client import Client
from fcfmramos.web_scraper.ucampus import Plan, RamoInPlan, Subplan
from bs4 import NavigableString


def get_plan_url(plan_id: str) -> str:
    return (
        f"https://ucampus.uchile.cl/m/fcfm_bia/recuento_uds?pla_id={plan_id}"
    )


async def scrape_plan(ucampus_client: Client, plan_id: str):

    url = get_plan_url(plan_id)

    soup = await ucampus_client.scrape(url)

    excel_table = soup.find("table", class_="excel")
    td_colspans2 = excel_table.find_all("td", colspan="2")
    tbodies = excel_table.find_all("tbody")

    plan = Plan(plan_id, [])

    for i in range(0, len(tbodies)):
        subplan = Subplan("", [], [])
        plan.suplanes.append(subplan)

        title = td_colspans2[i]
        subplan.subplan_name = "".join(
            [
                element
                for element in title
                if isinstance(element, NavigableString)
            ]
        ).strip()

        body = tbodies[i]

        for tr in body.find_all("tr"):
            second_td = tr.find_all("td")[1]
            anchor = second_td.find("a")

            if anchor:
                subplan.subplanes.append(anchor.text.strip())
            else:
                subplan.ramos.append(RamoInPlan(second_td.text.strip()))

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

    print(plan)

    # save plan to file
    with open(f"{plan_id}.json", "w") as file:
        file.write(str(plan))
