import httpx

async def get_core_web_vitals(url: str):

    api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    params = {
        "url": url,
        "category": "performance",
        "key": ""
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        response = await client.get(api, params=params)

    data = response.json()

    lighthouse = data["lighthouseResult"]
    audits = lighthouse["audits"]

    metrics = {
        "LCP": audits["largest-contentful-paint"]["displayValue"],
        "CLS": audits["cumulative-layout-shift"]["displayValue"],
        "TBT": audits["total-blocking-time"]["displayValue"],
        "FCP": audits["first-contentful-paint"]["displayValue"],
        "SpeedIndex": audits["speed-index"]["displayValue"]
    }

    score = lighthouse["categories"]["performance"]["score"] * 100

    return {
        "url": url,
        "performance_score": score,
        "metrics": metrics
    }