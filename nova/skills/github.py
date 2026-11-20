import os
import requests
import dotenv

dotenv.load_dotenv()

def github_notifications():
    token = os.getenv("GH_TOKEN")

    if not token:
        return {"error": "GitHub token missing"}

    try:
        response = requests.get(
            "https://api.github.com/notifications",
            headers={"Authorization": f"Bearer {token}"},
            params={"per_page": 50},
            timeout=10
        )

        response.raise_for_status()

        notifications = response.json()

        return {
            "count": len(notifications),
            "notifications": [
                {
                    "repository": n["repository"]["full_name"],
                    "title": n["subject"]["title"],
                    "type": n["subject"]["type"],
                    "reason": n["reason"]
                }
                for n in notifications
            ]
        }

    except requests.RequestException as e:
        return {"error": str(e)}