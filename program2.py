import requests
import csv

URL = "https://data.cdc.gov/resource/h3ej-a9ec.json"
MEASURE = "Depression among adults aged >=18 years"

def fetch_all_counties(year: int, outfile: str = "program2.csv"):
    params = {
        "year": str(year),
        "measure": MEASURE,
        "$limit": 50000
    }

    r = requests.get(URL, params=params)
    r.raise_for_status()
    data = r.json()

    rows = []

    for row in data:
        try:
            year = row["year"]
            state = row["statedesc"]
            abbr = row["stateabbr"]
            county = row["locationname"]
            percent = float(row["data_value"])
            population = int(row["totalpopulation"])
        except (KeyError, ValueError):
            continue

        rows.append({
            "year": year,
            "state": state,
            "state_abbr": abbr,
            "county": county,
            "percent_depression": percent,
            "total_population": population
        })

# needed to sort it
    rows.sort(key=lambda x: (x["state_abbr"], x["county"]))

    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "year",
                "state",
                "state_abbr",
                "county",
                "percent_depression",
                "total_population"
            ]
        )
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    fetch_all_counties(2021)
