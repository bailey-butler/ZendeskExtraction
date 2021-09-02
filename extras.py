import json
# import os
#
# with open("fields.json") as f:
#     raw_fields = json.load(f)
#     fields: dict[str, str] = {
#         int(field.get("id")): field.get("title") for field in raw_fields.get("ticket_fields")
#     }


def load_data(obj_type: str) -> dict[str, dict]:
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
#
#
# with open("groups.json") as f:
#     raw_groups = json.load(f)
#     groups: dict[str, dict] = {
#         int(group.get("id")): group for group in raw_groups.get("groups")
#     }
#
#
# user_page_n = 1
#
# users = {}
#
# while os.path.isfile(file_name := f"users.{user_page_n}.json"):
#     with open(file_name, encoding="utf-8") as f:
#         raw_users = json.load(f)
#         for user in raw_users.get("users"):
#             users[user.get("id")] = user
#     user_page_n += 1
#
#
# organization_page_n = 1
#
# organizations = {}
#
# while os.path.isfile(file_name := f"organizations.{organization_page_n}.json"):
#     with open(file_name, encoding="utf-8") as f:
#         raw_organizations = json.load(f)
#         for organization in raw_organizations.get("organizations"):
#             organizations[organization.get("id")] = organization
#     organization_page_n += 1
#
