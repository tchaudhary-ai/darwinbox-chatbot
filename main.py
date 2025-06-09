import logging
logging.basicConfig(level=logging.DEBUG)
import requests
from requests.auth import HTTPBasicAuth

CONFLUENCE_BASE_URL = "https://yourcompany.atlassian.net/wiki"
EMAIL = "your.email@yourcompany.com"
API_TOKEN = "ATATT3xFfGF0FoEsbUXPvqHHTHLjFZXfm_8zyu7V3dgBaJdLTBv_-m0k-0z0z-nExyXh9L2TlSut9JBgPNb8KzgKcFu_3zHmH-fzodUL1tivWq5DfIvgd9Ln_swNSOMCzRSx50ZYX4Me8MMVE0WzPKuO80SkvPi0EU813CiQx3FjjJPTmP6CFOo=03A2B0AD"

def search_confluence(query):
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/search"
    params = {
        "cql": f"text ~ \"{query}\" AND type=page",
        "limit": 1
    }
    auth = HTTPBasicAuth(EMAIL, API_TOKEN)
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            title = results[0]["title"]
            link = CONFLUENCE_BASE_URL + results[0]["_links"]["webui"]
            return f"I found something in Confluence: [{title}]({link})"
    return "I couldn't find anything relevant in Confluence."

@app.route("/", methods=["GET", "POST"])
def chatbot():
    response = ""
    if request.method == "POST":
        user_input = request.form["message"]
        response = get_response(user_input)
    return render_template("chat.html", response=response)

app.run(host='0.0.0.0', port=81)
