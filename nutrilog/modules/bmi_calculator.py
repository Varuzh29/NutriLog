def calculate_bmi(weight, height):
    bmi = round(weight / (height / 100) ** 2, 2)
    interpretation = None
    if bmi < 18.5:
        interpretation = "Underweight"
    elif 18.5 <= bmi < 25:
        interpretation = "Normal weight"
    elif 25 <= bmi < 30:
        interpretation = "Overweight"
    else:
        interpretation = "Obese"
    return {"index": bmi, "interpretation": interpretation}
