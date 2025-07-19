# CodeMentor AI

**CodeMentor AI** is an intelligent, full-stack web application that helps users learn, practice, and improve their coding skills with the help of advanced AI. It features an AI-powered code editor, voice-to-code functionality, coding challenges, progress tracking, and user profile management.

---

## 🚀 Features

- **AI Code Editor**: Write, debug, and improve code with real-time AI assistance. Supports Python, JavaScript, Java, C++, and C.
- **Voice-to-Code**: Generate code or prompts using your voice, powered by OpenAI Whisper.
- **Coding Challenges**: Practice with a curated set of challenges of varying difficulty, with instant feedback and progress tracking.
- **User Profiles**: Save code snippets, track solved challenges, and manage preferences (including dark mode).
- **Progress Dashboard**: Visualize your challenge progress and stats.
- **Authentication**: Secure registration, login, and password reset via email.
- **Modern UI**: Responsive, beautiful interface with dark mode support.

---

## 🛠 Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend**: Jinja2 templates, Bootstrap, CodeMirror, Chart.js
- **AI/ML**: Google Gemini API, OpenAI Whisper (for speech-to-text)
- **Database**: PostgreSQL (or any SQLAlchemy-compatible DB)
- **Other**: dotenv, SMTP for email, etc.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd codementor_ai
```
## 2. Install Dependencies

```bash
pip install -r requirements.txt
```
## 3. Environment Variables
Create a .env file in the root directory with the following content (adjust as needed):

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/codementor_ai
GOOGLE_API_KEY=your_google_gemini_api_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_email_password
FROM_EMAIL=your_email@gmail.com
```
## 4. Database Setup
Create the database and tables:
```bash
# Create the database in your SQL server (e.g., PostgreSQL)
# Then run:
psql -d codementor_ai -f create_tables.sql
```
## 5. Seed Coding Challenges
```bash
python seed.py
```
## 6. Run the Application
```bash
python -m app.run
```
Visit http://localhost:5000 in your browser.

---

## 💡 Usage

- Register for a new account or log in.
- Use the **AI Code Editor** to write code, ask for explanations, find bugs, or generate code from voice.
- Try **coding challenges** and track your progress.
- Save useful **code snippets** to your profile.
- Change your theme (**light/dark**) in your profile preferences.

---

## 🧱 Project Structure
codementor_ai/
├── app/
│ ├── init.py
│ ├── run.py
│ ├── models.py
│ ├── seed_challenges.py
│ ├── static/
│ └── templates/
├── config.py
├── create_tables.sql
├── requirements.txt
└── seed.py

---

## 📦 Data Models

- **User_details**: User info, email, password (hashed), preferences, and snippets.
- **Snippet**: Saved code snippets per user.
- **Challenge**: Coding challenges with starter code and test cases.
- **UserChallengeProgress**: Tracks user attempts, solutions, and feedback per challenge.

---

## 🔑 Key Files

- `app/run.py`: Main Flask app, routes, and logic.
- `app/models.py`: SQLAlchemy models.
- `app/seed_challenges.py`: Challenge seeding logic.
- `app/templates/`: Jinja2 HTML templates for all pages.
- `app/static/`: CSS and static assets.
- `create_tables.sql`: SQL schema for the database.
- `requirements.txt`: Python dependencies.

---

## 🤖 AI & Voice Features

- **AI Code Assistance**: Uses Google Gemini API for code explanations, improvements, and bug finding.
- **Voice-to-Code**: Uses OpenAI Whisper for speech-to-text, allowing hands-free code generation and prompts.

---

## 🔐 Security

- Passwords are hashed using Werkzeug.
- Session management via Flask-Login.
- Password reset via secure email token.

---

## 🛠 Customization

- Add more challenges in `app/seed_challenges.py`.
- Adjust UI in `app/templates/` and `app/static/`.
- Extend AI capabilities by integrating other APIs.

---

## 📄 License

(Add your license here, e.g., MIT, GPL, etc.)

---

## 🙏 Credits

- Flask  
- Google Gemini  
- OpenAI Whisper  
- CodeMirror  
- Bootstrap  
- Chart.js

---

## 🐛 Troubleshooting

- Make sure you have `ffmpeg` installed for audio conversion (required by Whisper).
- Ensure your database URL and API keys are correct in `.env`.
- For email features, use an app password if using Gmail with 2FA.


