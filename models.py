from pydantic import BaseModel, Field

class UserInput(BaseModel):
    age: int = Field(..., description="年齡（單位：歲）")
    height: float = Field(..., description="身高（單位：cm）")
    weight: float = Field(..., description="體重（單位：kg）")
    gender: str = Field(..., description="性別：male 或 female")
    activity_level: str = Field(..., description="活動等級：sedentary, light, moderate, active, very_active")
    goal: str = Field(..., description="目標：cut（減脂）、maintain（維持）、bulk（增肌）")

class TdeeResponse(BaseModel):
    bmr: float
    tdee: float
    recommended_calories: float
    message: str
    bmi: float
    bmi_message: str