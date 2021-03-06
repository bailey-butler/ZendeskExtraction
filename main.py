import csv
import json
import os.path
import time

from progressbar import progressbar, Bar

from extras import fields, users, groups, organizations, tickets
from retrieve import retrieve_and_save


# Meta

# Ticket columns to be included in extract; excludes custom fields
headers = [
    "id",
    "created_at",
    "updated_at",
    "subject",
    "description",
    "priority",
    "status",
    "requester_id",
    "submitter_id",
    "assignee_id",
    "organization_id",
    "group_id",
    "tags"
]

# Comment columns to be included in extract
comment_headers = [
    "id",
    "type",
    "author_id",
    "body",
    "public",
    "created_at"
]

# List of columns to be replaced by user values
user_keys = [
    "requester_id",
    "submitter_id",
    "assignee_id",
    "author_id"
]

# List of columns to be replaced by group values
group_keys = [
    "group_id"
]

# List of columns to be replaced by organisation values
organization_keys = [
    "organization_id"
]


# Function to update dynamic columns (user, group, organisation) replacing ID with title/meaningful value
def replace(key: str, value: str) -> list[tuple[str, str]]:
    if key in user_keys:
        if value in users:
            new_key = key.split("_")[0]
            user = users.get(value)
            return [
                (f"{new_key}", user.get("name")),
                (f"{new_key}_email", user.get("email")),
                (f"{new_key}_id", user.get("id"))
            ]
        return [(key, "")]

    if key in group_keys:
        if value in groups:
            return [(key, groups.get(value).get("name"))]
        return [(key, "")]

    if key in organization_keys:
        if value in organizations:
            return [(key, organizations.get(value).get("name"))]
        return [(key, "")]

    if key == "tags":
        return [(key, ",".join(value))]

    return [(key, value)]


all_tickets: list[dict] = []
all_comments: list[dict] = []

# Iterate over every ticket, get specified columns and save all comments
for ticket_id, ticket in progressbar(tickets.items()):
    # Skip over scam Russian entries
    if any(flagged in ticket["description"] for flagged in [".ru/", ".ru.", ".r/", ".su/"]):
        continue

    # Clean up ticket
    this_ticket = {
        new_header: new_value for header in headers for new_header, new_value in replace(header, ticket.get(header))
    } | {
        fields.get(field.get("id")).get("title"): field.get("value") for field in ticket.get("fields")
    }
    all_tickets.append(this_ticket)

    # Retrieve comments
    all_comments += [
        {
            new_header: new_value for header in comment_headers for new_header, new_value in replace(header, comment.get(header))
        } | {
            "ticket_id": ticket_id
        } for comment in retrieve_and_save("comments", endpoint=f"tickets/{ticket_id}/comments", save=False)
    ]

keys = all_tickets[93].keys()

with open("tickets.csv", "w", newline="", encoding="utf-8") as f:
    dw = csv.DictWriter(f, keys)
    dw.writeheader()
    dw.writerows(all_tickets)


comments_keys = all_comments[0].keys()

with open("comments.csv", "w", newline="", encoding="utf-8") as f:
    dw = csv.DictWriter(f, comments_keys)
    dw.writeheader()
    dw.writerows(all_comments)
