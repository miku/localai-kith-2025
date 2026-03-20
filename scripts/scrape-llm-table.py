#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas", "lxml", "requests", "tabulate"]
# ///

import argparse
import datetime
import pandas as pd
import requests
from io import StringIO
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Wikipedia's list of large language models")
    parser.add_argument("-a", "--all", action="store_true", help="list all models, not just free/open ones")
    args = parser.parse_args()

    page = "https://en.wikipedia.org/wiki/List_of_large_language_models"
    html = StringIO(requests.get(page, headers={"User-agent": "Mozilla/5.0"}).text)
    dfs = pd.read_html(html)
    if len(dfs) < 1:
        raise ValueError(f"could not fetch: {page}")
    df = next(d for d in dfs if "Name" in d.columns and "Developer" in d.columns)
    print("\n".join(df.columns.tolist()), file=sys.stderr)
    with open(f"{datetime.date.today()}-wikipedia-list-of-llm.md", "w") as f:
        proprietary_labels = [
            "Proprietary",
            "Unreleased",
            "Proprietary[57]",
            "Non-commercial research[d]",
        ]
        out = df[["Name", "Release date[a]", "Developer", "License[c]"]]
        if not args.all:
            out = out[~df["License[c]"].isin(proprietary_labels)]
        out["Developer"] = out["Developer"].str.slice(0, 12)
        out["License[c]"] = out["License[c]"].str.slice(0, 20)
        out.reset_index(drop=True, inplace=True)
        out.to_markdown(f)
        f.write("\n")
