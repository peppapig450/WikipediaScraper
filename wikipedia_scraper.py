import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


class WikipediaScrapingError(Exception):
    pass


def get_wikipedia_table(url: str):
    # Fetch the wikipedia page
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except requests.HTTPError as e:
        raise WikipediaScrapingError(
            f"Something went wrong getting the content of the url: {url}"
        ) from e

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all tables in the page
    tables = soup.select("table.wikitable")
    dataframes: list[pd.DataFrame] = []
    for table in tables:
        df = pd.read_html(StringIO(str(table)))[0]
        dataframes.append(df)
    return dataframes


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/List_of_missions_to_the_Moon"
    dataframes = get_wikipedia_table(url)
    target_df = dataframes[0]
    print(target_df.info(verbose=True))
    print(target_df)
