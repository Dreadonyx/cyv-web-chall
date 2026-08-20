import base64
import secrets
from pathlib import Path

from flask import Flask, Response, abort, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = False


@app.get("/")
def index():
    return redirect(url_for("view_documents"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") != "user" or request.form.get("password") != "user@123":
            return render_template("login.html", error="Invalid username or password."), 401
        response = redirect(url_for("view_documents"))
        response.set_cookie("session_id", secrets.token_urlsafe(24), httponly=True, samesite="Lax")
        response.set_cookie("role", base64.b64encode(b"user").decode("ascii"), httponly=True, samesite="Lax")
        return response
    return render_template("login.html", error=None)


@app.get("/view")
def view_documents():
    filename = request.args.get("file")
    if not filename:
        documents = sorted(item.name for item in DOCS_DIR.iterdir() if item.is_file())
        return render_template(
            "view.html",
            documents=documents,
            logged_in=bool(request.cookies.get("session_id")),
        )

    # Intentional CTF vulnerability: user input is joined directly to docs.
    target = DOCS_DIR / filename
    try:
        content = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        abort(404)
    return Response(content, mimetype="text/plain")



@app.get("/admin")
def admin():
    role_cookie = request.cookies.get("role", "")
    try:
        role = base64.b64decode(role_cookie, validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        abort(403)

    if role != "admin":
        abort(403)
    return render_template("admin.html")


@app.get("/logout")
def logout():
    response = redirect(url_for("login"))
    response.delete_cookie("session_id")
    response.delete_cookie("role")
    return response


@app.errorhandler(403)
def forbidden(_error):
    return render_template("error.html", code=403, message="Forbidden"), 403


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", code=404, message="Not found"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
