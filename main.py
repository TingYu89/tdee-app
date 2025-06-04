from fastapi import FastAPI
from models import UserInput, TdeeResponse
from calculator import calculate_bmr_tdee, calculate_bmi, get_bmi_advice
from recommender import get_recommended_calories
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn
import os
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

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

@app.post("/ask-ai")
async def ask_ai(data: dict):
    user_prompt = f"我是一位{data['age']}歲的{data['gender']}，我目前的TDEE是{data['tdee']}，我的目標是{data['goal']}。請給我一天的飲食與運動建議，請具體並簡潔地列出重點。"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        # "HTTP-Referer": "https://yourdomain.onrender.com",
        "X-Title": "tdee-app"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "你是一位營養師與運動教練，請根據使用者提供的TDEE資訊提供具體建議。"},
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        ai_reply = response.json()["choices"][0]["message"]["content"]
        return JSONResponse(content={"ai_response": ai_reply})
    else:
        return JSONResponse(status_code=500, content={"error": "API call failed"})