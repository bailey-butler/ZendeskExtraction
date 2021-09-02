import json
import os

import retrieve


def load_data(obj_type: str) -> dict[str, dict]:
    if not os.path.exists(f"data/{obj_type}.json"):
        retrieve.retrieve_and_save(obj_type, save=True)

    with open(f"data/{obj_type}.json") as f:
        raw_data = json.load(f)
    data: dict[str, dict] = {
        row.get("id"): row for row in raw_data
    }
    return data


fields = load_data("ticket_fields")
groups = load_data("groups")
users = load_data("users")
organizations = load_data("organizations")
tickets = load_data("tickets")
