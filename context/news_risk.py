"""News Risk Module - integruojasi su forex-news konteineriu"""
import httpx
from datetime import datetime, timedelta


async def get_news_risk(news_api_url: str = "http://192.168.0.187:8000/api/news") -> dict:
    """
    Tikrina naujienų riziką iš forex-news konteinerio
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(news_api_url, timeout=5)
            if response.status_code == 200:
                news = response.json()
                high_impact = [n for n in news if n.get("importance") == "High"]

                # Apskaičiuojam minutes iki artimiausios High impact naujienos
                minutes_to_next = 999
                risk_level = "low"

                if high_impact:
                    risk_level = "high" if len(high_impact) > 2 else "medium"

                return {
                    "risk_level": risk_level,
                    "minutes_to_next": minutes_to_next,
                    "high_impact_count": len(high_impact),
                    "total_news": len(news)
                }
    except Exception:
        pass

    return {"risk_level": "unknown", "minutes_to_next": 999, "high_impact_count": 0, "total_news": 0}
