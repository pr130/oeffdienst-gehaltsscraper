from py.fun import * 

import polars as pl

# einzelner abruf
scrape_gehaltsrechner(stufe=2)

# mehrere Abfragen auf einmal mit loop
konfigs = [(gruppe, stufe, prozent) for gruppe in range(12, 13) for stufe in range(1,2) for prozent in range(50, 105, 5)]

gehaelter = []
for konfig in konfigs:
    print(f"getting {konfig}")
    gehalt = scrape_gehaltsrechner(
        gruppe=konfig[0],
        stufe=konfig[1],
        steuerkl=1,
        zeit=konfig[2],
        kinderfb=0
    )
    gehaelter.append(gehalt)
#turn into data frame
gehaelter_df = pl.DataFrame(gehaelter)
print(gehaelter_df)
gehaelter_df.write_csv("data/2024-09-test-python.csv")
