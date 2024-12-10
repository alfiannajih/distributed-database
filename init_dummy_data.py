import requests
import json

with open("dummy_restok.jsonl", "r") as fp:
    for line in fp:
        dummy_restok = json.loads(line)

        requests.post(
            "http://localhost:8000/api/restock",
            json=dummy_restok
        )
        
with open("dummy_orders.jsonl", "r") as fp:
    for line in fp:
        dummy_order = json.loads(line)

        requests.post(
            "http://localhost:8000/api/orders",
            json=dummy_order
        )