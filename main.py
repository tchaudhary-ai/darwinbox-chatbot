from flask import Flask, render_template, request

app = Flask(__name__)

# Simple chatbot logic
def get_response(user_input):
    if "leave policy" in user_input.lower():
        return "You can find the leave policy here: https://confluence.company.com/leave-policy"
    elif "holiday list" in user_input.lower():
        return "Here is the holiday list: https://confluence.company.com/holidays"
    else:
        return "Sorry, I didn't understand that. Try asking about leave policy or holiday list."

@app.route("/", methods=["GET", "POST"])
def chatbot():
    response = ""
    if request.method == "POST":
        user_input = request.form["message"]
        response = get_response(user_input)
    return render_template("chat.html", response=response)

app.run(host='0.0.0.0', port=81)