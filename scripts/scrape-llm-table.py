#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas", "lxml", "requests", "tabulate"]
# ///

import datetime
import pandas as pd
import requests
from io import StringIO

if __name__ == '__main__':
    page = "https://en.wikipedia.org/wiki/List_of_large_language_models"
    html = StringIO(requests.get(page, headers={'User-agent': 'Mozilla/5.0'}).text)
    dfs = pd.read_html(html)
    if len(dfs) < 1:
        raise ValueError(f"could not fetch: {page}")
    df = dfs[0]
    with open(f"{datetime.date.today()}-wikipedia-list-of-llm.md", "w") as f:
        df[["Name", "Release date[a]", "License[c]"]][df["License[c]"] != "Proprietary"].to_markdown(f)
        f.write("\n")
