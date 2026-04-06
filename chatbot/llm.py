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
        print("USING GROK API")

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
                    "content": "You are a friendly Indian doctor. Talk in Hinglish. Give simple and practical advice."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload, timeout=8)

        print("STATUS:", response.status_code)

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]

        return None

    except Exception as e:
        print("GROK ERROR:", e)
        return None


# ================= LOCAL SMART SEARCH =================
def get_local_response(user_message):

    print("USING LOCAL DATA")

    user_message = user_message.lower()

    results = []

    for disease, info in health_data.items():

        disease_name = disease.lower()
        symptoms_text = info.get('symptoms_en', '').lower()
        treatment = info.get('treatment_en', '')
        medicines_list = info.get('medicines', [])

        symptoms_list = [s.strip() for s in symptoms_text.split(",")]
        medicines_lower = [m.lower() for m in medicines_list]

        score = 0

        # -- Disease match
        if disease_name in user_message:
            score += 3

        # ----Symptoms match
        for sym in symptoms_list:
            if sym in user_message:
                score += 1

        # --Medicine match
        for med in medicines_lower:
            if med in user_message:
                score += 2

        if score > 0:
            results.append({
                "disease": disease,
                "score": score,
                "symptoms": symptoms_text,
                "medicines": ", ".join(medicines_list),
                "treatment": treatment
            })

    if not results:
        return None

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    response = ""

    for res in results[:3]:
        response += f"""Possible Disease: {res['disease']}

Symptoms:
{res['symptoms']}

Medicines:
{res['medicines']}

Treatment:
{res['treatment']}

------------------------

"""

    return response.strip()


# ================= MAIN FUNCTION =================
def get_ai_response(user_message):

    user_message = user_message.lower().strip()

    ai_reply = get_grok_response(user_message)

    if ai_reply:
        return {"reply": ai_reply}
    
    local_reply = get_local_response(user_message)

    if local_reply:
        return {"reply": local_reply}

    
    return {"reply": "I'm not sure. Please consult a doctor."}
