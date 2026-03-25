import json
import os
import requests

# ================= LOCAL DATA =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "health_data.json")

with open(file_path, encoding="utf-8") as f:
    health_data = json.load(f)

# ================= GROK API =================
XAI_API_KEY = "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"

def get_grok_response(user_message):
    try:
        url = "https://api.x.ai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {XAI_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "grok-beta",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a friendly doctor. Talk like a real human. Give simple, natural and helpful medical advice."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]

        return None

    except Exception as e:
        print("GROK ERROR:", e)
        return None


# ================= LOCAL FALLBACK =================
def get_local_response(user_message):

    for disease in health_data:

        info = health_data[disease]

        if disease in user_message:

            symptoms = info.get('symptoms_en', '')
            treatment = info.get('treatment_en', '')
            medicines = ", ".join(info.get('medicines', []))

            return f"""
You may have {disease}.

Symptoms:
{symptoms}

Medicines:
{medicines}

Treatment:
{treatment}

If condition worsens, consult a doctor.
""".strip()

    return None


# ================= MAIN FUNCTION =================
def get_ai_response(user_message):

    user_message = user_message.lower().strip()

    # -------------------------
    # GROK FIRST
    # -------------------------
    ai_reply = get_grok_response(user_message)

    if ai_reply:
        return ai_reply

    # -------------------------
    # LOCAL FALLBACK
    # -------------------------
    local_reply = get_local_response(user_message)

    if local_reply:
        return local_reply

    # -------------------------
    # FINAL FALLBACK
    # -------------------------
    return "I'm not sure. Please consult a doctor."

