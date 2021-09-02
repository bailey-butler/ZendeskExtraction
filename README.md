# Zendesk Extract

Script to extract Ticket and Comment object from Zendesk


## Setup

Environment variables must be set (or saved in `.env`):
 - `ZENDESK_EMAIL` containing the email address
 - `ZENDESK_TOKEN` containing the API token, retrieved through their web portal


## Run

Run `main.py` to save all data.

Ticket data will be saved to `tickets.csv`, comment data will be saved to `comments.csv`.
Accessory data will be stored in `data` folder.

```shell
python3 main.py
```
