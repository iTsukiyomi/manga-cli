import requests
import time

BASE_URL = "https://api.mangadex.org"
_RATE_LIMIT_DELAY = 0.25 # in seconds

def _get(endpoint: str, params: dict | None = None):
    """ makes a get requests and return a parsed json """
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        time.sleep(_RATE_LIMIT_DELAY)
        return response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"API error {response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Runtime error: {e}")
    
def search_manga(query: str, limit: int = 20):
    """ search for manga by title """
    data = _get("/manga",{
        "title": query,
        "limit": limit,
        "order[relevance]": "desc",
        "includes[]": ["cover_arts"],
    })

    results = []

    for item in data.get("data", []):
        attrs = item.get("attributes", {})

        titles = attrs.get("title", {})
        title = (
            titles.get("en")
            or titles.get("ja-ro")   # romanized Japanese
            or next(iter(titles.values()), "Unknown Title")
        )
        
        status = attrs.get("status", "unknown")
        last_chp = attrs.get("lastChapter") or "?"

        cover_filename = None
        for rel in item.get("relationships", []):
            if rel["type"] == "cover_art":
                cover_filename = rel.get("attributes", {}).get("fileName")
                break
        
        results.append({
            "id": item["id"],
            "title": title,
            "status": status,
            "last_chapter": last_chp,
            "cover_filename": cover_filename,
            "description": _get_description(attrs),
        })

    return results

def _get_description(attrs: dict) -> str:
    """Extract English description, falling back to first available."""
    desc = attrs.get("description", {})
    return (
        desc.get("en")
        or next(iter(desc.values()), "No description available.")
    )