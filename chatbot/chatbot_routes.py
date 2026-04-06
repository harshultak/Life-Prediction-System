from flask import Blueprint, request, jsonify
from .llm import get_ai_response

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

@chatbot_bp.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"reply": "Please enter a health question."})

    reply = get_ai_response(user_message)

    return jsonify(reply)   
