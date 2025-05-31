from models import UserInput

activity_factors = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9
}

def calculate_bmr_tdee(data: UserInput):
    if data.gender.lower() == "male":
        bmr = 10 * data.weight + 6.25 * data.height - 5 * data.age + 166
    else:
        bmr = 10 * data.weight + 6.25 * data.height - 5 * data.age - 161

    factor = activity_factors.get(data.activity_level.lower(), 1.2)
    tdee = bmr * factor
    recommended_calories = tdee
    if data.goal == "cut":
        recommended_calories = tdee - 500
        message = f"為了減脂，建議你每日攝取約 TDEE - 500，即 {recommended_calories:.2f} kcal。請維持蛋白質攝取並減少油脂與糖。"
    elif data.goal == "bulk":
        recommended_calories = tdee + 300
        message = f"為了增肌，建議你每日攝取約 TDEE + 300，即 {recommended_calories:.2f} kcal。請注意攝取足夠蛋白質與總熱量。"
    else:
        message = f"維持體重建議每日攝取 TDEE 即可，即 {recommended_calories:.2f} kcal，保持均衡飲食。"
    bmi = calculate_bmi(data.weight, data.height)
    bmi_message = get_bmi_advice(bmi)
    return bmr, tdee, recommended_calories, message, bmi, bmi_message


def calculate_bmi(weight: float, height: float) -> float:
    height_m = height / 100  # cm to meters
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_advice(bmi: float) -> str:
    if bmi < 18.5:
        return "您的 BMI 偏低，建議增加熱量以增重。"
    elif 18.5 <= bmi < 24:
        return "您的 BMI 正常，維持目前的飲食與運動習慣即可。"
    elif 24 <= bmi < 27:
        return "您的 BMI 略高，建議略為減重。"
    else:
        return "您的 BMI 偏高，建議減重，並搭配運動調整。"