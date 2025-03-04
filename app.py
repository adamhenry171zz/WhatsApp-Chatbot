from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

def generate_ai_response(user_message):
    """Generate a smart AI response using OpenAI."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI chatbot for an online shopping business. Answer customer queries professionally."},
                {"role": "user", "content": user_message}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "Sorry, I'm having trouble responding right now. Please try again later."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """Handle incoming WhatsApp messages and respond using AI."""
    incoming_msg = request.values.get("Body", "").strip()
    response = MessagingResponse()
    
    if incoming_msg:
        bot_reply = generate_ai_response(incoming_msg)
        response.message(bot_reply)
    else:
        response.message("I didn't understand that. Can you please rephrase?")
    
    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
