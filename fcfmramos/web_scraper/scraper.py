from bs4 import BeautifulSoup, element

from fcfmramos.web_scraper.client import Client
from fcfmramos.web_scraper.ucampus import (
    get_catalogo_url,
    Catalogo,
    Ramo,
    Curso,
    Profesor,
    Departamento,
)


async def scrape(client: Client, url: str) -> BeautifulSoup:
    response_code, html = await client.get(url)
    if response_code != 200:
        print(f"Failed to fetch {url} with response code {response_code}")
    return BeautifulSoup(html, "html.parser")  # TODO: test swapping for lxtml


def extract_programa_id(url: str) -> int | None:
    return None if not url else int(url[url.find("id=") + 3:])


def text_from_dt_dd(dl: element.Tag, title: str) -> str | None:
    dt = dl.find("dt", string=title)
    if dt is None:
        return None
    dd = dt.find_next_sibling("dd")
    return dd.get_text() if dd else None


def url_from_dt_dd_a(dl: element.Tag, title: str) -> str | None:
    dt = dl.find("dt", string=title)
    if dt is None:
        return None
    dd = dt.find_next_sibling("dd")
    return dd.find("a")["href"] if dd and dd.a else None


def get_ramo_codigo(element: element.Tag) -> str:
    return element.find("div", class_="objeto")["id"]


def get_ramo_nombre(element: element.Tag) -> str:
    return (
        element.find("h1")
        .text.strip()
        .splitlines()[0]
        .replace(get_ramo_codigo(element), "", 1)  # todo: inefficient
        .strip()
    )


def get_ramo_sustentabilidad(element: element.Tag) -> bool:
    return element.find("span", class_="sustentable") is not None


def get_ramo_creditos(element: element.Tag) -> int:
    ramo_dl = element.find("dl", class_="leyenda")
    return int(text_from_dt_dd(ramo_dl, "Créditos:"))


def get_ramo_requisitos(element: element.Tag) -> str:
    ramo_dl = element.find("dl", class_="leyenda")
    return text_from_dt_dd(ramo_dl, "Requisitos:")


def get_ramo_equivalencias(element: element.Tag) -> list[str] | None:
    ramo_dl = element.find("dl", class_="leyenda")
    equivalencias_string = text_from_dt_dd(ramo_dl, "Equivalencias")
    return (
        None if not equivalencias_string else equivalencias_string.split("/")
    )


def get_ramo_comentario(element: element.Tag) -> str | None:
    ramo_dl = element.find("dl", class_="leyenda")
    return text_from_dt_dd(ramo_dl, "Comentario")


def get_ramo_programa(element: element.Tag) -> int | None:
    ramo_dl = element.find("dl", class_="leyenda")
    programa_url = url_from_dt_dd_a(ramo_dl, "Programa:")
    return extract_programa_id(programa_url)


def get_curso_cupos(element: element.Tag) -> int:
    return int(element.get_text(strip=True))


def get_curso_modalidad(element: element.Tag) -> str | None:
    h1 = element.find("h1")
    em = h1.find("em")
    return em.get_text(strip=True) if em else None


def get_curso_comentario(element: element.Tag) -> str | None:
    h2 = element.find("h2")
    return h2.get_text(strip=True) if h2 else None


def get_curso_profesores(element: element.Tag) -> list[Profesor]:
    profesores: list[Profesor] = []
    profe_list = element.find("ul", class_="profes").find_all("li")

    for profe in profe_list:
        img = profe.find("img")
        src = img["src"]
        profe_id = src.split("/")[-3]
        nombre = profe.find("h1").get_text(strip=True)

        profesores.append(Profesor(profe_id, nombre))

    return profesores


def get_curso_programa(element: element.Tag, programa_ramo: int) -> int | None:
    h1 = element.find("h1")
    programa_element = h1.find("a")
    if programa_element:
        return extract_programa_id(programa_element["href"])
    else:
        return programa_ramo


def get_curso_horarios(element: element.Tag) -> str | None:
    horario_element = element.find("div", title=True)
    return horario_element["title"].strip() if horario_element else None


async def scrape_catalogo(
    client: Client, semester: int, department: Departamento
) -> Catalogo:
    ramos: list[Ramo] = []

    soup = await scrape(client, get_catalogo_url(semester, department.id))
    catalogo = soup.find(id="body")

    ramo_divs = catalogo.find_all("div", class_="ramo")

    for ramo_div in ramo_divs:
        cursos: list[Curso] = []
        programa = get_ramo_programa(ramo_div)

        cursos_table = ramo_div.find("table", class_="cursos").tbody
        seccion = 0
        for curso_tr in cursos_table.find_all("tr"):
            seccion += 1
            curso_tds = curso_tr.find_all("td")

            cursos.append(
                Curso(
                    seccion,
                    get_curso_cupos(curso_tds[1]),
                    get_curso_cupos(curso_tds[2]),
                    get_curso_programa(curso_tds[0], programa),
                    get_curso_modalidad(curso_tds[0]),
                    get_curso_comentario(curso_tds[0]),
                    get_curso_profesores(curso_tds[0]),
                    get_curso_horarios(curso_tds[3]),
                )
            )

        ramos.append(
            Ramo(
                get_ramo_codigo(ramo_div),
                get_ramo_nombre(ramo_div),
                get_ramo_creditos(ramo_div),
                get_ramo_comentario(ramo_div),
                get_ramo_sustentabilidad(ramo_div),
                get_ramo_requisitos(ramo_div),
                get_ramo_equivalencias(ramo_div),
                cursos,
            )
        )

    return Catalogo(semester, department, ramos)
