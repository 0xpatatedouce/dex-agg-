#!/usr/bin/env python3

import time, requests

API_KEY   = "3lTqlUuhHrgwGONwF1JED19xK7kGgJfF"
QUERY_ID  = 3437314
HEADERS   = { "x-dune-api-key": API_KEY }
BASE_URL  = "https://api.dune.com/api/v1"

def run_query():
    r = requests.post(f"{BASE_URL}/query/{QUERY_ID}/execute", headers=HEADERS)
    r.raise_for_status()
    execution_id = r.json()["execution_id"]

    while True:
        resp = requests.get(f"{BASE_URL}/execution/{execution_id}/status", headers=HEADERS)
        resp.raise_for_status()
        status = resp.json().get("state")
        if status in ("QUERY_STATE_FINISHED", "QUERY_STATE_FAILED"):
            break
        time.sleep(2)

    if status != "QUERY_STATE_FINISHED":
        raise RuntimeError(f"La requête a échoué (status: {status})")

    res = requests.get(f"{BASE_URL}/execution/{execution_id}/results", headers=HEADERS)
    res.raise_for_status()
    return res.json()["result"]["rows"]

if __name__ == "__main__":
    data = run_query()
    print(data)






