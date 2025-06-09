import os
import logging
import requests
from flask import Flask, render_template, request
from requests.auth import HTTPBasicAuth

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)

# Load sensitive values from environment variables
CONFLUENCE_BASE_URL = "https://ocrolus.atlassian.net/wiki"
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("API_TOKEN")

# Function to search Confluence using REST API
def search_confluence(query):
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/search"
    params = {
        "cql": f'text ~ "{query}" AND type=page',
        "limit": 1
    }
    auth = HTTPBasicAuth(EMAIL, API_TOKEN)
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, auth=auth, params=params)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                title = results[0]["title"]
                link = CONFLUENCE_BASE_URL + results[0]["_links"]["webui"]
                return f"I found something in Confluence: <a href='{link}' target='_blank'>{title}</a>"
            else:
                return "No relevant pages found in Confluence."
        else:
            return f"Confluence API returned an error: {response.status_code}"
    except Exception as e:
        logging.error(f"Error calling Confluence API: {e}")
        return "There was an error searching Confluence."

# Main route
@app.route("/", methods=["GET", "POST"])
def chatbot():
    response = ""
    if request.method == "POST":
        user_input = request.form["message"]
        response = search_confluence(user_input)
    return render_template("chat.html", response=response)
    
