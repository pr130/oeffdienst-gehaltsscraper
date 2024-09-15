from typing_extensions import TypedDict, NotRequired
import re
import requests
from bs4 import BeautifulSoup


class GehaltsDict(TypedDict):
    id: NotRequired[str]
    ag_brutto: float
    an_brutto: float
    an_netto: float
    sv_ag: float
    sv_an: float
    lohnsteuer: float
    soli: float
    abzuege_gesamt: float


def get_gruppen(id_vertrag: str = "tvoed-bund-2024"):
    # TODO
    return "https://oeffentlicher-dienst.info/c/t/rechner/tvoed/bund?id=tvoed-bund-2024&matrix=1"


def make_url(
    gruppe: int = 13,
    stufe: int = 3,
    steuerkl: int = 1,
    zeit: float = 100.0,
    kinderfb: float = 0,
) -> str:
    """
    Erstellt die URL gegeben die Parameter der Stelle.
    :param str gruppe: TvöD-Gruppe. Valide Werte abhängig vom Tarifvertrag: z.B. "E13" oder "E9a". Komplette Liste: siehe get_gruppen(id_vertrag)
    :param int stufe: TvöD-Stufe. Valide Werte: 1-6
    :param int steuerkl: Steuerklasse. Valide Werte: 0-6
    :param float zeit: Arbeitszeit in %. Valide Werte: 0-100%
    :param float kinderfb: Kinderfreibeträge. Valide Werte: 0-9,5 in 0,5 Schritten.
    :return str: URL für die Detailseite für die Konfiguration.
    """

    # TODO: nicht nur tvöd 2024, Krankenkasse, Zusatzversorgung, Kinder für Pflegeversicherung, Kirchensteuer
    url = f"https://oeffentlicher-dienst.info/c/t/rechner/tvoed/bund?id=tvoed-bund&g=E_{gruppe}&s={stufe}&zv=keine&z={zeit}&zulage=&stkl={steuerkl}&r=0&zkf={kinderfb}&kk=15.5%25"
    return url


def get_eur(main_table_txt: str, search_for: str):
    """
    Extrahiert einen bestimmten Euro-Wert basierend auf dem Begriff, der davor steht, aus der Detailseite für die Stellenkonfiguration.
    :param str main_table_txt: String, der den gesamten Text der Detailseite enthält
    :param str search_for: Begriff vor dem Doppelpunkt, z.B. "Lohnsteuer" oder "Monats-Brutto"
    :return float: Betrag in Euro
    """
    r = f"{search_for}\\:?\\s+\\-?\\s+(\\d+\\.?\\d.+?)"
    return float(re.search(r, main_table_txt).groups()[0])


def extract_values(main_table_txt: str) -> GehaltsDict:
    """
    Extrahiert alle relevanten Werte aus der Detailseite.
    :param str main_table_txt: String, der den gesamten Text der Gehalts"tabelle" der Detailseite enthält
    :return GehaltsDict: Dictionary mit Gehaltsbestandteilen
    """
    data = {
        "an_brutto": get_eur(main_table_txt, "Monats-Brutto"),
        "an_netto": get_eur(main_table_txt, "netto bleiben"),
        "lohnsteuer": get_eur(main_table_txt, "Lohnsteuer"),
        "soli": get_eur(main_table_txt, "Solidaritätszuschlag"),
        "abzuege_gesamt": get_eur(main_table_txt, "Abzüge gesamt"),
    }
    data["sv_an"] = round(data["abzuege_gesamt"] - data["soli"] - data["lohnsteuer"], 2)
    data["sv_ag"] = round(data["an_brutto"] * 1.21 - data["an_brutto"], 2)
    data["ag_brutto"] = round(data["an_brutto"] + data["sv_ag"], 2)

    return data


def get_table_txt(url: str):
    """
    Scrapt die Detailseite und extrahiert die "Tabelle" mit den Gehaltsdetails.
    :param str url: URL der Detailseite, siehe make_url
    :return str table_txt: String, der den gesamten Text der Gehalts"tabelle" der Detailseite enthält
    """
    # get HTML text
    html_txt = requests.get(url).content
    h = BeautifulSoup(html_txt, "html.parser")
    main_table_txt = h.find_all("table")[0].get_text()  # first table
    return main_table_txt


def scrape_gehaltsrechner(
    gruppe: int = 13,
    stufe: int = 3,
    steuerkl: int = 1,
    zeit: float = 100.0,
    kinderfb: float = 0,
) -> GehaltsDict:
    """
    Scrapt die Gehaltskomponenten für die Stellenkonfiguration. 
    :param str gruppe: TvöD-Gruppe. Valide Werte abhängig vom Tarifvertrag: z.B. "E13" oder "E9a". Komplette Liste: siehe get_gruppen(id_vertrag)
    :param int stufe: TvöD-Stufe. Valide Werte: 1-6
    :param int steuerkl: Steuerklasse. Valide Werte: 0-6
    :param float zeit: Arbeitszeit in %. Valide Werte: 0-100%
    :param float kinderfb: Kinderfreibeträge. Valide Werte: 0-9,5 in 0,5 Schritten.
    :return GehaltsDict: Dictionary mit Gehaltskomponenten für die Stellenonfiguration.
    """
    url = make_url(gruppe, stufe=stufe, steuerkl=steuerkl, zeit=zeit, kinderfb=kinderfb)

    main_table_txt = get_table_txt(url)
    data = extract_values(main_table_txt)
    data["id"] = f"E{gruppe}-{stufe}-{zeit}-stkl{steuerkl}-{kinderfb}"

    return data
