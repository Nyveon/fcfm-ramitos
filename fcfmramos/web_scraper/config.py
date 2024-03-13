from pathlib import Path

FCFM_CATALOGO_URL = "https://ucampus.uchile.cl/m/fcfm_catalogo/"
FCFM_SALAS_URL = "https://ucampus.uchile.cl/m/fcfm_eventos/objeto?objeto=sala-"
FCFM_CURSOS_URL = "https://www.u-cursos.cl/ingenieria/2/cursos_departamento/"
SEMESTERS = [20221]
DEPARTMENTS = [5]  # TODO: get departments from the website
CACHE_DIR = Path() / ".cache"

if not CACHE_DIR.exists():
    CACHE_DIR.mkdir()
