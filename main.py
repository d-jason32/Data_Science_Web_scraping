import requests
import csv
import time

# the RestAPI that we are collecting data from
url = "https://data.cdc.gov/resource/5eh7-pjx8.json"


# the cdc survey question from the RestAPI
survey = (
    "During the past 30 days, how many days did poor physical or mental health keep you from doing your usual activities, such as self-care, work, or recreation?"
)

# we will iterate through all the 50 states
states = [
    "AL", "AK",
    "AZ", "AR",
    "CA", "CO",
    "CT", "DE",
    "FL", "GA",
    "HI", "ID",
    "IL", "IN",
    "IA", "KS",
    "KY", "LA",
    "ME", "MD",
    "MA", "MI",
    "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]


def get_info(state_abbr: str, year: int, question_text: str):
    # building the API query
    params = {
        "$select": (
            "year, area, area_abbr, question, percent, "
            "low_confidence_interval, high_confidence_interval, "
            "confidence_interval_formatted"
        ),
        "$where": (
            f"area_abbr='{state_abbr.upper()}' "
            f"AND year='{year}' "
            f"AND question='{question_text}'"
        )
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    # returns the response from the api
    return response.json()


def fetch_all_states(year: int, question: str, outfile: str = "survey.csv"):
    results = []

    for state in states:
        rows = get_info(state, year, question)
        if rows:
            results.append(rows[0])


    # entering the data to the API
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "year",
                "area",
                "area_abbr",
                "question",
                "percent",
                "low_confidence_interval",
                "high_confidence_interval",
                "confidence_interval_formatted"
            ]
        )
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    fetch_all_states(2023, survey)
