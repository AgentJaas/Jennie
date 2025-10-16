import os
from openai import OpenAI
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# --- Initialize OpenAI client ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Flask route for WhatsApp webhook ---
@app.route("/webhooks/twilio", methods=["POST"])
def reply_whatsapp():
    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")

    print(f"💬 Incoming from {sender}: {incoming_msg}")

    # --- Build response ---
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # --- Send user message to OpenAI ---
        prompt = f"""
        You are Jennie, an upbeat, efficient executive assistant.
        You're friendly, proactive, and always ready to help people
        be more productive. Keep replies short, natural, and helpful.

        User: {incoming_msg}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        reply = response.choices[0].message.content.strip()
        msg.body(reply)

    except Exception as e:
        print("❌ Error:", e)
        msg.body("Sorry, something went wrong. Please try again later.")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)