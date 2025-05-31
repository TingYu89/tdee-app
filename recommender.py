def get_recommended_calories(tdee: float, goal: str):
    goal = goal.lower()
    if goal == "cut":
        recommended = tdee - 500
        msg = f"為了減重，建議你每日攝取約 TDEE - 500，即 {round(recommended, 2)} kcal。請維持蛋白質攝取並減少油脂與糖。"
    elif goal == "bulk":
        recommended = tdee + 300
        msg = f"為了增肌，建議你每日攝取約 TDEE + 300，即 {round(recommended, 2)} kcal。記得多攝取蛋白質與碳水。"
    else:
        recommended = tdee
        msg = f"維持體重建議每日攝取 TDEE 即可，即 {round(recommended, 2)} kcal，保持均衡飲食。"
    
    return round(recommended, 2), msg