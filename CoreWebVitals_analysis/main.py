from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from psi_service import get_core_web_vitals
from ai_service import generate_seo_explanation
from visualization import generate_visualization
import os

app = FastAPI()

app.mount("/charts", StaticFiles(directory="charts"), name="charts")

@app.get("/analyze")
async def analyze(url: str):
    try:
        psi_data = await get_core_web_vitals(url)

        explanation = await generate_seo_explanation(
            url,
            psi_data["metrics"],
            psi_data["performance_score"]
        )

        viz = generate_visualization(
            psi_data["metrics"],
            psi_data["performance_score"]
        )

        chart_urls = {}
        for chart_type, filepath in viz["charts"].items():
            filename = os.path.basename(filepath)
            chart_urls[chart_type] = f"/charts/{filename}"

        return {
            "url": url,
            "performance_score": psi_data["performance_score"],
            "metrics": psi_data["metrics"],
            "ai_explanation": explanation,
            "visualization": {
                "chart_urls": chart_urls,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chart/{chart_name}")
async def get_chart(chart_name: str):
    chart_path = os.path.join("charts", chart_name)
    if os.path.exists(chart_path):
        return FileResponse(chart_path)
    return {"error": "Chart not found"}
