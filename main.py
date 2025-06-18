import os
import logging
import requests
from flask import Flask, render_template, request
from requests.auth import HTTPBasicAuth

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

# Lattice credentials
LATTICE_API_TOKEN = os.getenv("LATTICE_API_TOKEN")
LATTICE_BASE_URL = "https://api.latticehq.com/v1"

# Get user profile by email
def get_user_profile(email):
    headers = {"Authorization": f"Bearer {LATTICE_API_TOKEN}"}
    params = {"email": email}
    url = f"{LATTICE_BASE_URL}/users"
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        users = res.json().get("data", [])
        return users[0] if users else None
    else:
        logging.error(f"User fetch failed: {res.text}")
        return None

# Get latest review summary for the user
def get_last_review_summary(user_id):
    headers = {"Authorization": f"Bearer {LATTICE_API_TOKEN}"}
    url = f"{LATTICE_BASE_URL}/reviews?user_id={user_id}"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        reviews = res.json().get("data", [])
        if reviews:
            last_review = reviews[-1]
            summary = last_review.get("summary") or "No summary available."
            return summary
        else:
            return "No reviews found for this user."
    else:
        logging.error(f"Review fetch failed: {res.text}")
        return "Error fetching review summary."

@app.route("/", methods=["GET", "POST"])
def chatbot():
    response = ""
    if request.method == "POST":
        email = request.form["message"].strip()
        user = get_user_profile(email)
        if user:
            name = user.get("name")
            title = user.get("title")
            department = user.get("department")
            user_id = user.get("id")

            review_summary = get_last_review_summary(user_id)

            response = f"""
            ✅ <strong>Found user: {name}</strong><br>
            👤 Email: {email}<br>
            🧩 Title: {title}<br>
            🏢 Department: {department}<br>
            📝 <strong>Last Review Summary:</strong><br>{review_summary}
            """
        else:
            response = f"❌ No user found for email: {email}"
    return render_template("chat.html", response=response)
