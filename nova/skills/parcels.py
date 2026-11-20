import requests
import os
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

def get_parcels():
    output = subprocess.run(
        ["shop", "order", "search"],
        capture_output=True,
        text=True
    )

    data = json.loads(output.stdout)["data"]

    parcels = []

    for item in data.get("orders", []) + data.get("shipments", []):
        fulfillment = item.get("fulfillment", {})
        events = item.get("fulfillment", {}).get("events") or []
        tracking_number = events[0].get("tracking_number") if events else None

        parcels.append({
            "name": item.get("label"),
            "status": item.get("delivery_status") or item.get("status"),
            "order_placed_at": item.get("placed_at"),
            "arrives": [
                e.get("description")
                for e in fulfillment.get("expectations", [])
            ],
            "latest_status": package_status(tracking_number) if tracking_number else None
            
        })

    return parcels

def package_status(tracking_number: str):

    res = requests.get(
        f"https://api.lastscanned.com/v1/track/{tracking_number}",
        headers={"Authorization": f"Bearer {os.getenv('LASTSCANNED_KEY')}"},
    )
    try:
        res.raise_for_status()
    except requests.HTTPError as e:
        print(e)
    return(res.json())
