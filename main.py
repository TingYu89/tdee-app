from fastapi import FastAPI
from models import UserInput, TdeeResponse
from calculator import calculate_bmr_tdee, calculate_bmi, get_bmi_advice
from recommender import get_recommended_calories
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="TDEE Calculator",
    description="輸入你的基本資料與目標，我們將計算你的 BMR、TDEE 並提供建議熱量攝取值。",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/tdee", response_model=TdeeResponse,
    summary="計算 BMR、TDEE 並回傳建議攝取熱量",
    description="輸入年齡、身高、體重、性別、活動量與目標（減脂、維持、增肌），回傳對應建議。")

def compute_tdee(data: UserInput):
    bmr, tdee, recommended_calories, message, bmi, bmi_message = calculate_bmr_tdee(data)
    recommended_calories, message = get_recommended_calories(tdee, data.goal)
    bmi = calculate_bmi(data.weight, data.height)
    bmi_msg = get_bmi_advice(bmi)

    return TdeeResponse(
        bmr=bmr,
        tdee=tdee,
        recommended_calories=recommended_calories,
        message=message,
        bmi=bmi,
        bmi_message=bmi_msg,
    )

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/exercise", response_class=HTMLResponse)
def exercise_page(request: Request):
    return templates.TemplateResponse("exercise.html", {"request": request})