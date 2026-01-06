import joblib
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# ================= LOAD MODEL =================
model = joblib.load("model/model.pkl")
features = joblib.load("model/features.pkl")

# ================= LOAD DATA =================
data = pd.read_csv("life_expectancy_preprocessed.csv")
country_list = sorted(data["Country"].unique())

# ================= HELPERS =================
smoking_map = {"none": 0.0, "light": 0.5, "regular": 1.0}

def normalize_income(country_data, income_level):
    avg = float(country_data["Income_Composition_Of_Resources"].iloc[0])
    levels = {
        "very_low": avg * 0.45,
        "low": avg * 0.75,
        "medium": avg,
        "high": min(avg * 1.25, 0.9),
        "very_high": min(avg * 1.55, 0.95),
    }
    return levels.get(income_level, avg)

def generate_health_advice(bmi, smoking, alcohol):
    factors = []
    recommendations = []

    if bmi < 18.5:
        factors.append({"type": "negative", "title": "Low BMI"})
        recommendations.append({"title": "Improve Nutrition"})
    elif bmi <= 24.9:
        factors.append({"type": "positive", "title": "Healthy BMI"})
    else:
        factors.append({"type": "negative", "title": "High BMI"})
        recommendations.append({"title": "Weight Management"})

    if smoking != "none":
        factors.append({"type": "negative", "title": "Smoking"})
        recommendations.append({"title": "Quit Smoking"})
    else:
        factors.append({"type": "positive", "title": "Non-Smoker"})

    if alcohol > 7:
        factors.append({"type": "negative", "title": "High Alcohol Intake"})
        recommendations.append({"title": "Reduce Alcohol"})
    else:
        factors.append({"type": "positive", "title": "Moderate Alcohol Intake"})

    return factors, recommendations

# ================= ROUTES =================
@app.route("/")
def index():
    return render_template(
        "life-expectancy-calculator.html",
        countries=country_list
    )

@app.route("/predict", methods=["POST"])
def predict():
    d = request.get_json()

    age = int(d["age"])
    country = d["country"]
    height = float(d["height"])
    weight = float(d["weight"])
    smoking = d["smoking"]
    alcohol = float(d["alcohol"])
    schooling = float(d["education"])
    income = d["income"]

    bmi = weight / ((height / 100) ** 2)

    country_data = data[
        (data["Country"] == country) & (data["Year"] == 2015)
    ]

    if country_data.empty:
        return jsonify({"error": "Country not found"}), 400

    smoking_score = (
        float(country_data["Smoking_Rate"].iloc[0]) *
        smoking_map.get(smoking, 0)
    )

    alcohol_year = alcohol * 0.0158 * 52
    income_norm = normalize_income(country_data, income)

    row = {}
    for f in features:
        if f == "BMI":
            row[f] = bmi
        elif f == "Alcohol":
            row[f] = alcohol_year
        elif f == "Schooling":
            row[f] = schooling
        elif f == "Income_Composition_Of_Resources":
            row[f] = income_norm
        elif f == "Smoking_Rate":
            row[f] = smoking_score
        else:
            row[f] = float(country_data[f].iloc[0])

    df = pd.DataFrame([row])
    prediction = round(float(model.predict(df)[0]), 1)

    factors, recommendations = generate_health_advice(
        bmi, smoking, alcohol
    )

    # ✅ KEY FIX HERE
    return jsonify({
        "result": prediction,
        "factors": factors,
        "recommendations": recommendations
    })

@app.route("/result")
def result():
    # ✅ KEY FIX HERE
    predicted = request.args.get(
        "predicted_life_expectancy", type=float
    )
    age = request.args.get("age", type=int)

    if predicted is None or age is None:
        return "Missing data", 400

    years_left = predicted - age
    percent = (age / predicted) * 100 if predicted > 0 else 0

    return render_template(
        "result.html",
        predicted_life_expectancy=predicted,
        age=age,
        years_left=round(years_left, 1),
        percent_lived=round(percent, 1)
    )

if __name__ == "__main__":
    app.run(debug=True)
