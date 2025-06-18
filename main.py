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

# Function to check Lattice API connectivity using /v1/users
def get_lattice_status():
    url = "https://api.latticehq.com/v1/users"
    headers = {
        "Authorization": f"Bearer {LATTICE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        logging.debug(f"Lattice API response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            users = data.get("data", [])
            if not users:
                return "✅ Connected to Lattice, but no users found."
            first_user = users[0]
            email = first_user.get("email", "N/A")
            name = first_user.get("name", "N/A")
            return f"✅ Lattice API is working!<br><br>👤 First user: <b>{name}</b><br>📧 Email: {email}"
        else:
            logging.error(f"Lattice API error {response.status_code}: {response.text}")
            return f"❌ Lattice API error {response.status_code}: {response.text}"
    except Exception as e:
        logging.error(f"Exception while calling Lattice API: {e}")
        return f"❌ Exception while calling Lattice: {e}"

# Main chatbot route
@app.route("/", methods=["GET", "POST"])
def chatbot():
    response = ""
    if request.method == "POST":
        user_input = request.form["message"]
        response = get_lattice_status()  # Email input is not used in this test
    return render_template("chat.html", response=response)
