import os
import logging
import requests
from flask import Flask, render_template, request

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)

# Load Lattice API key from environment
LATTICE_API_KEY = os.getenv("LATTICE_API_KEY")

# Function to fetch a user by their email from Lattice
def get_user_by_email(input_email):
    url = "https://api.latticehq.com/v1/users"
    headers = {
        "Authorization": f"Bearer {LATTICE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            users = data.get("data", [])

            # Loop through users to find the one that matches the input email
            for user in users:
                if user.get("email", "").lower() == input_email.lower():
                    name = user.get("name", "N/A")
                    title = user.get("title", "N/A")
                    department = user.get("department", "N/A")
                    return (
                        f"✅ Found user: <strong>{name}</strong><br>"
                        f"📧 Email: {input_email}<br>"
                        f"🧑‍💼 Title: {title}<br>"
                        f"🏢 Department: {department}"
                    )

            return f"❌ No user found with email: {input_email}"
        else:
            logging.error(f"Lattice API error {response.status_code}: {response.text}")
            return f"❌ Lattice API error {response.status_code}: {response.text}"
    except Exception as e:
        logging.error(f"Exception while calling Lattice API: {e}")
        return f"❌ Error: {e}"

# Main chatbot route
@app.route("/", methods=["GET", "POST"])
def chatbot():
    response = ""
    if request.method == "POST":
        user_input = request.form["message"]
        response = get_user_by_email(user_input)
    return render_template("chat.html", response=response)
