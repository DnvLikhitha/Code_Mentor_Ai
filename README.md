# CodeMentor AI

CodeMentor AI is an intelligent coding assistant and practice platform. It combines a robust Flask backend with a beautiful, modern React frontend to deliver AI-powered coding challenges, voice-to-code transcription, and real-time code analysis.

## Features

- **Interactive Code Editor**: Write and test code right in the browser with beautiful syntax highlighting.
- **AI-Powered Mentorship**: Highlight code to get explanations, find bugs, or receive suggestions for improvement using Google's Gemini models.
- **Voice-to-Code**: Speak your logic out loud! CodeMentor AI uses Whisper to transcribe your voice and convert it directly into executable code.
- **Challenge Arena**: Test your skills with algorithmic challenges across multiple difficulties (Easy, Medium, Hard).
- **Progress Tracking**: Keep track of your solved challenges, failed attempts, and overall skill breakdown on a personalized dashboard.
- **Snippet Library**: Save helpful code snippets (along with AI-generated explanations) directly to your profile.
- **Modern UI/UX**: Built with React, Tailwind CSS, and Lucide Icons for a premium, glassmorphism-inspired dark mode experience.

## Technology Stack

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- TypeScript
- React Router DOM
- Axios

**Backend:**
- Python & Flask
- SQLite / SQLAlchemy (Database)
- Google Generative AI (Gemini 2.5 Flash)
- OpenAI Whisper (Voice-to-Text)

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm
- FFmpeg (Required for Whisper voice transcription)

### 1. Backend Setup

Clone the repository and install the Python dependencies:

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the root directory (make sure not to commit this!) and add your API keys:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Initialize the database and start the Flask API:
```bash
python -m app.run
```
*The backend API will start on `http://localhost:5000`.*

### 2. Frontend Setup

Open a new terminal window, navigate to the frontend directory, and start the Vite development server:

```bash
cd frontend
npm install
npm run dev
```
*The frontend will be available at `http://localhost:5173`.*

## Security Note
Ensure your `.env` file is always included in your `.gitignore`. Never commit your API keys to version control.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request for new features, bug fixes, or improvements.
