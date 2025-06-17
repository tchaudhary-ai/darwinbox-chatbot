import os
import logging
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv  # Optional: for local development

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)

# Load Lattice API key from environment
LATTICE_API_KEY = os.getenv("LATTICE_API_KEY")

# Function to call Lattice API and fetch performance review summary
def get_review_summary(email):
    url = "https://api.latticehq.com/v1/reviews"  # Adjust if Lattice gives a different endpoint
    headers = {
        "Authorization": f"Bearer {LATTICE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Example logic – update based on actual structure
            for review in data.get("data", []):
                if review.get("employee", {}).get("email") == email:
                    summary = review.get("summary", "No summary available.")
                    return f"📄 Latest performance summary for {email}:<br><br>{summary}"

            return "No performance review found for this email."
        else:
            logging.error(f"Lattice API error {response.status_code}: {response.text}")
            return f"Lattice API returned an error: {response.status_code}"
    except Exception as e:
        logging.error(f"Error calling Lattice API: {e}")
        return "There was an error fetching data from Lattice."

# Main chatbot route
@app.route("/", methods=["GET", "POST"])
def chatbot():
    response = ""
    if request.method == "POST":
        user_input = request.form["message"]
        response = get_review_summary(user_input)
    return render_template("chat.html", response=response)
