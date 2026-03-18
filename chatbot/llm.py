import json
import os

# Get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build path to health_data.json
file_path = os.path.join(BASE_DIR, "health_data.json")

# Load dataset
with open(file_path, encoding="utf-8") as f:
    health_data = json.load(f)


def get_ai_response(user_message):

    user_message = user_message.lower().strip()

    # -------------------------
    # 1️⃣ Disease search
    # -------------------------
    for disease in health_data:

        info = health_data[disease]

        if disease in user_message:

            symptoms_en = info.get('symptoms_en', 'No data available')
            symptoms_hi = info.get('symptoms_hi', '')

            treatment_en = info.get('treatment_en', 'No data available')
            treatment_hi = info.get('treatment_hi', '')

            doctor_en = info.get('doctor_en', 'Consult a doctor if symptoms worsen')
            doctor_hi = info.get('doctor_hi', '')

            medicines = ", ".join(info.get('medicines', []))

            response = f"""
Disease: {disease}

Symptoms:
{symptoms_en}
{symptoms_hi}

Medicines:
{medicines}

Treatment:
{treatment_en}
{treatment_hi}

Doctor Advice:
{doctor_en}
{doctor_hi}
"""

            return response.strip()

    # -------------------------
    # 2️⃣ Medicine search
    # -------------------------
    for disease in health_data:

        info = health_data[disease]

        medicines = info.get("medicines", [])

        for med in medicines:

            if med.lower() in user_message:

                symptoms_en = info.get('symptoms_en', '')
                symptoms_hi = info.get('symptoms_hi', '')

                response = f"""
Medicine: {med}

Used For Disease:
{disease}

Symptoms:
{symptoms_en}
{symptoms_hi}
"""

                return response.strip()

    return "Please ask a health related question."
