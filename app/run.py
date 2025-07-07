from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests

from app.models import db, User_details

app = Flask(__name__)
app.secret_key = "supersecretkey"
load_dotenv()

# Make sure to initialize db with app somewhere (if not using factory)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["password"]

        # Check if user already exists
        if User_details.query.filter_by(email=email).first():
            error = "Email already registered."
        elif password != confirm:
            error = "Passwords do not match."
        else:
            hashed_pw = generate_password_hash(password)
            user = User_details(name=name, email=email, password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
    return render_template('register.html', error=error)

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User_details.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for("editor"))
        else:
            error = "Incorrect email or password."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route('/editor')
def editor():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return render_template("editor.html")

# Mock AI endpoints
@app.route("/api/<action>", methods=["POST"])
def api_action(action):
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "python")
    hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
    headers = {"Authorization": f"Bearer {hf_api_key}"}

    # Choose a Hugging Face model for code (StarCoder, CodeGen, etc.)
    model_id = "tiiuae/falcon-7b-instruct"

    # Prompt templates for each action
    prompts = {
        "explain": f"Explain in plain English what this {language} code does:\n{code}",
        "doc": f"Generate documentation (docstrings or comments) for this {language} code:\n{code}",
        "errors": f"Detect and highlight syntax issues in this {language} code. Explain the errors:\n{code}",
        "improve": (
            f"Suggest better variable names, formatting, and structure for this {language} code. "
            f"Identify redundant logic and propose simplification. Predict and fill in incomplete code if any:\n{code}"
        ),
        "debug": (
            f"Find bugs in this {language} code, suggest fixes, and explain likely root causes. "
            f"Give enhanced debugging tips:\n{code}"
        ),
    }
    prompt = prompts.get(action, f"Analyze this {language} code:\n{code}")

    # Hugging Face Inference API call
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model_id}",
        headers=headers,
        json={"inputs": prompt}
    )

    if response.status_code == 200:
        result = response.json()
        # Hugging Face returns a list of dicts with 'generated_text'
        if isinstance(result, list) and "generated_text" in result[0]:
            output = result[0]["generated_text"]
        else:
            output = str(result)
    else:
        output = f"Error: {response.status_code} {response.text}"

    return {"result": output}

@app.route('/profile')
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user = User_details.query.get(session["user_id"])
    snippets = user.snippets if user else []
    return render_template("profile.html", user=user, snippets=snippets)

if __name__ == '__main__':
    app.run(debug=True)