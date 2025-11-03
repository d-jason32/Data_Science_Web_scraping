import requests

url = "https://data.cdc.gov/resource/5eh7-pjx8.json"

survey = (
    "During the past 30 days, how many days did poor physical or mental health keep you from doing your usual activities, such as self-care, work, or recreation?"
)

def get_info(state_abbr: str, year: int, question_text: str):
    parameter = {
        "$select":
        (
            "year, "
            "area, "
            "area_abbr, "
            "question, "
            "percent, "
            "low_confidence_interval, "
            "high_confidence_interval, "
            "confidence_interval_formatted"
        ),
        "$where": (
            f"area_abbr='{state_abbr.upper()}' "
            f"AND year='{year}' "
            f"AND question='{question_text}'"
        )
    }

    response = requests.get(url, params=parameter)

    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    rows = get_info("NY", 2023, survey)

    if rows:
        r = rows[0]
        print(
            f"{r['year']} "
            f"{r['area_abbr']} "
            f"({r['area']}): "
            f"{r['percent']}% "
        )
