import time
from datetime import datetime, timezone

from flask import Flask, render_template, request, redirect, url_for, make_response

import session as sess

app = Flask(__name__)

FLAG = open("/flag.txt", "r", encoding="utf-8").read()


users = {}
welcome_feed = []  

def add_user(username: str, pw: str, created_at: int):
    users[username] = {"pw": pw, "created_at": created_at}
    welcome_feed.append({"username": username, "created_at": created_at})


if "admin" not in users:
    add_user("admin", "**REDACTED**", int(time.time()))


def current_user():
    s = request.cookies.get("session", "")
    parsed = sess.parse_session(s)
    if not parsed:
        return None

    username, _ = parsed
    u = users.get(username)
    if not u:
        return None

    return sess.verify_session(s, u["created_at"])


@app.get("/")
def index():
    uname = current_user()
    return render_template("index.html", username=uname, is_admin=(uname == "admin"), flag=FLAG)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username").strip()
    pw = request.form.get("password")

    if not username or not pw:
        return redirect(url_for("register"))
    if username in users:
        return "Already exists"

    created_at = int(time.time())
    add_user(username, pw, created_at)

    resp = make_response(redirect(url_for("welcome")))
    resp.set_cookie("session", sess.make_session(username, created_at))
    return resp


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username").strip()
    pw = request.form.get("password")

    u = users.get(username)
    if not u or u["pw"] != pw:
        return "fail"

    resp = make_response(redirect(url_for("welcome")))
    resp.set_cookie("session", sess.make_session(username, u["created_at"]))
    return resp


@app.get("/welcome")
def welcome():
    uname = current_user()
    if not uname:
        return redirect(url_for("login"))

    feed = []
    for row in welcome_feed:
        e = row["created_at"]
        dt = datetime.fromtimestamp(e, tz=timezone.utc).strftime("%d/%m/%Y, %H:%M:%S UTC")
        feed.append({"username": row["username"], "created_at_str": dt})

    return render_template("welcome.html", username=uname, users=feed)


@app.get("/logout")
def logout():
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie("session", "", expires=0)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
