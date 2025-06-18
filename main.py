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

    found_user = None
    starting_after = None

    try:
        while True:
            params = {"limit": 100}
            if starting_after:
                params["starting_after"] = starting_after

            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                logging.error(f"Lattice API error {response.status_code}: {response.text}")
                return f"❌ Lattice API error {response.status_code}: {response.text}"

            data = response.json()
            users = data.get("data", [])
            has_more = data.get("has_more", False)

            for user in users:
                email = user.get("email", "").strip().lower()
                logging.debug(f"Checking Lattice user: {email}")
                if email == input_email.strip().lower():
                    found_user = user
                    break

            if found_user or not has_more:
                break

            if users:
                starting_after = users[-1].get("id")

        if found_user:
            name = found_user.get("name", "N/A")
            title = found_user.get("title", "N/A")
            department = found_user.get("department", "N/A")
            return (
                f"✅ Found user: <strong>{name}</strong><br>"
                f"📧 Email: {found_user.get('email')}<br>"
                f"🧑‍💼 Title: {title}<br>"
                f"🏢 Department: {department}"
            )
        else:
            return f"❌ No user found with email: {input_email}"

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
