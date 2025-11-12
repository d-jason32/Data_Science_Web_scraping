import requests
import csv

# BRFSS Chronic Health Indicators RestAPI
url = "https://chronicdata.cdc.gov/resource/dttw-5yxu.json"

# The question from the survey
DEPRESSION_Q = "Ever told you that you have a form of depression?"

# All 50 states (two-letter abbreviations)
states = [
    "AL","AK",
    "AZ","AR",
    "CA","CO",
    "CT","DE",
    "FL","GA",
    "HI","ID",
    "IL","IN",
    "IA","KS",
    "KY","LA",
    "ME","MD",
    "MA","MI",
    "MN","MS",
    "MO","MT",
    "NE","NV",
    "NH","NJ",
    "NM","NY",
    "NC","ND",
    "OH","OK",
    "OR","PA",
    "RI","SC",
    "SD","TN",
    "TX","UT",
    "VT","VA",
    "WA","WV",
    "WI","WY"
]

def get_info(state_abbr: str, year: int, question_text: str):
    params = {
        "$select": "year, locationdesc, locationabbr, data_value",
        "$where": (
            f"locationabbr='{state_abbr.upper()}' "
            f"AND year='{year}' "
            f"AND topic='Depression' "
            f"AND question='{question_text}' "
            f"AND response='Yes' "
            f"AND break_out='Overall' "
            f"AND break_out_category='Overall' "
            f"AND data_value_type='Crude Prevalence' "
            f"AND class='Chronic Health Indicators'"
        ),
        "$limit": 1
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

def fetch_all_states(year: int, question: str, outfile: str = "program1.csv"):
    results = []

    for abbr in states:
        rows = get_info(abbr, year, question)
        if rows:
            row = rows[0]
            results.append({
                "year": row.get("year"),
                "state": row.get("locationdesc"),
                "state_abbr": row.get("locationabbr"),
                "percent_yes": row.get("data_value")
            })

    # Write CSV with only 4 columns
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["year","state","state_abbr","percent_yes"])
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    fetch_all_states(2023, DEPRESSION_Q)