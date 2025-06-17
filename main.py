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

# Function to call Lattice API and fetch review cycle summary
def get_latest_review_cycle(email):
    url = "https://api.latticehq.com/v1/review_cycles"  # Valid endpoint
    headers = {
        "Authorization": f"Bearer {LATTICE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # If no review cycles found
            if not data:
                return f"No review cycles found for {email}."

            # Just show the most recent one (first in list)
            latest = data[0]
            name = latest.get("name", "Unnamed")
            status = latest.get("status", "Unknown")
            start = latest.get("start_date", "N/A")
            end = latest.get("end_date", "N/A")

            return (
                f"📄 Latest Review Cycle:<br><br>"
                f"<strong>{name}</strong><br>"
                f"🗓️ Status: {status}<br>"
                f"🕒 Start: {start}<br>"
                f"🕒 End: {end}"
            )
        else:
            logging.error(f"Lattice API error {response.status_code}: {response.text}")
            return f"Lattice API returned an error: {response.status_code}"
    except Exception as e:
        logging.error(f"Exception while calling Lattice API: {e}")
        return "There was an error fetching data from Lattice."

# Main chatbot route
@app.route("/", methods=["GET", "POST"])
def chatbot():
    response = ""
    if request.method == "POST":
        user_input = request.form["message"]
        response = get_latest_review_cycle(user_input)
    return render_template("chat.html", response=response)
