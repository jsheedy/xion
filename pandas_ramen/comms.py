import json
import re

import pandas as pd


def read_comms(fname: str = "comms.json"):
    with open(fname) as f:
        return json.load(f)


def parse_comms(comms):
    for i, row in enumerate(comms):
        if row["body"].lower().startswith("rating"):
            body_lines = [line.strip() for line in row["body"].split("\n")]
            rating_line = body_lines[0].strip()
            match = re.match(
                r"rating[ :]+([\.\w]+)([\.\n]?)", rating_line, re.IGNORECASE
            )
            if match:
                rating = match.groups()[0]
                body_lines[0] = rating_line[match.end():].strip()
            else:
                rating = "n/a"

            yield {
                "rating": rating.strip(),
                "author": row["name"],
                "created_at": row["datetime"],
                "comms_index": i,
                "title": row["subject"],
                "content": "\n".join(l.strip() for l in body_lines if l).strip(),
            }


def get_comms_df():
    return pd.DataFrame(parse_comms(read_comms()))
