
# oeffdienst-gehaltsscraper
![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg)

Funktionen und Skripte, um [oeffentlicher-dienst.info](https://oeffentlicher-dienst.info/) zu scrapen. Nützlich z.B. zur Stellenplanung im NPO-Kontext, wenn verschiedene Konstellationen durchgeplant werden müssen.

:warn: Bitte verantwortungsbewusst mit den Skripten umgehen und mit Bedacht scrapen. :warn:

Bisher sind nur Funktionen in Python verfügbar. Eine Übersetzung in R ist relativ einfach machbar (Relevante Packages: `rvest`, `stringr`). 

## Setup
Package management ist mit [`uv`](https://docs.astral.sh/uv/#getting-started).

```
uv sync
```


## Benutzung

In `scrape-py.qmd` und `scrape-py.py` finden sich Beispiele zur Benutzung.

```
python

## Begriffe

- _Detailseite_: Seite mit den Gehaltsbestandteilen für eine bestimmte Stellenkonfiguration, z.B. [hier](https://oeffentlicher-dienst.info/c/t/rechner/tvoed/bund?id=tvoed-bund&g=E_13&s=3&zv=keine&z=100&zulage=&stkl=1&r=0&zkf=0&kk=15.5%25)
- _Stellenkonfiguration_: eine bestimmte Kombination aus den folgenden Merkmalen:
    - Tarifvertrag (derzeit nur TvöD 2024)
    - Gruppe
    - Stufe
    - Arbeitszeit
    - Zusatzversorgung (derzeit nur "keine")
    - sonstigen Zulagen (derzeit nur "keine")
    - Steuerklasse
    - Kirchensteuer (derzeit nur "keine")
    - Kinder für Pflegeversicherung (derzeit nur "keine")
    - Krankenkassenbeitrag (derzeit nur 15,5%)
