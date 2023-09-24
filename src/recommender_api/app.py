# app.py
import utils
from flask import render_template  # Remove: import Flask
import connexion
from connexion.exceptions import OAuthProblem

TOKEN_DB = utils.open_files(file="security")

def apikey_auth(token, required_scopes):
    info = TOKEN_DB.get(token, None)
    if not info:
        raise OAuthProblem("Invalid token")

    return info

app = connexion.App(__name__, specification_dir="./")
app.add_api("../../swagger.yml")

@app.route("/")
def home():
    pass
    # return render_template("home.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
