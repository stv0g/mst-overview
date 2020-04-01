#!/usr/bin/env python3

from pathlib import Path
from typing import Union

import pandas
import yaml
from jinja2 import Template
from pandas import DataFrame


def read_csv_somacos(path: Union[Path, str]) -> DataFrame:
    # The dtype For the leading zeroes
    df = pandas.read_csv(path, dtype={"ags": "string"})
    df = df[["name", "ags", "vendor", "url"]]
    return df[(df["vendor"] == "somacos")]


def get_possible() -> DataFrame:
    """
    Check the scraped vendor info from the last two weeks and returns all where at least two weeks have a concensus
    """
    # Get the paths of the last three files
    [back2_path, back1_path, current_path] = sorted(
        Path("../ris-vendor-stats/").glob("*.csv")
    )[-3:]

    # Read it into one big JOIN
    back2 = read_csv_somacos(back2_path)
    back1 = read_csv_somacos(back1_path)
    current = read_csv_somacos(current_path)

    merged = pandas.merge(
        current, back1, how="outer", on=["name", "ags"], suffixes=["0", "1"]
    )
    merged = pandas.merge(
        merged, back2, how="outer", on=["name", "ags"], suffixes=["", "2"]
    )

    # If the current week was equal to one of the last weeks, take it as confirmed
    prior_confirmation = (merged["url"] == merged["url0"]) | (
        merged["url"] == merged["url1"]
    )
    confirmed_by_prior = merged[prior_confirmation][["name", "ags", "url"]]

    # Maybe the current week is wrong, but there is concensus between the prior two
    last_two_concensus = merged[
        ~prior_confirmation & (merged["url0"] == merged["url1"])
    ]
    last_two_concensus = last_two_concensus[["name", "ags", "url0"]].rename(
        columns={"url0": "url"}
    )

    print(
        f"Concensus with this week {len(confirmed_by_prior)}. Concensus in last two weeks: {len(last_two_concensus)}"
    )
    return pandas.concat([confirmed_by_prior, last_two_concensus]).sort_values("name")


def main():
    template = Path("index-template.jinja2").read_text()

    existing = pandas.read_csv("existing.csv").fillna("")
    cities = list(existing[["name", "ris", "url", "comment"]].T.to_dict().values())
    possible_cities = list(get_possible()[["name", "url"]].T.to_dict().values())

    oparl_cities = yaml.safe_load(Path("../resources/endpoints.yml").read_text())
    Path("index.html").write_text(
        Template(template).render(
            cities=cities, possible_cities=possible_cities, oparl_cities=oparl_cities
        )
    )


if __name__ == "__main__":
    main()
