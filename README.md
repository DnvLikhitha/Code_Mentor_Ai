---
title: CodeMentor AI
emoji: 🎓
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1.0"
python_version: "3.10"
pinned: false
---

# CodeMentor AI - Hugging Face Spaces

Deploy CodeMentor AI on Hugging Face Spaces using Docker.

## 🚀 Deploy on Hugging Face Spaces

### Step 1: Create a Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Configure:
   - **Space name**: `codementor-ai`
   - **License**: Select your preferred license
   - **Space SDK**: Choose **Docker**
   - **Space hardware**: **CPU** (sufficient to start)
4. Click **"Create Space"**

### Step 2: Clone and Push Code

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/codementor-ai
cd codementor-ai

# Copy your project files (app/, config.py, requirements.txt, Dockerfile, .dockerignore)
# Then push to HF Spaces
git add .
git commit -m "Deploy CodeMentor AI"
git push
```

### Step 3: Set Environment Variables

In your Space **Settings** → **Repository secrets**, add:

```
DATABASE_URL=postgresql://user:password@host:5432/dbname
GOOGLE_API_KEY=your_api_key_here
SECRET_KEY=your_secure_secret_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
```

**Database Options:**
- PostgreSQL/MySQL (external) - recommended for production
- SQLite with persistent storage at `/data/app.db`

### Step 4: Deploy

HF Spaces will automatically build and deploy your Docker container. Monitor the build in the Space logs.

## 📋 Requirements

- Python 3.10+
- Flask with SQLAlchemy
- PostgreSQL/MySQL or SQLite database
- Google Generative AI API key
- SMTP configured for email features

## 🔧 Key Configuration

- **Port**: 7860 (HF Spaces default)
- **Database**: External database recommended (set `DATABASE_URL`)
- **Static Files**: Served from `app/static/`
- **Templates**: Located in `app/templates/`

## 📚 Features

✅ User authentication and registration  
✅ AI-powered code challenges  
✅ Voice-to-code capability (Whisper)  
✅ Progress tracking  
✅ Password reset via email  
✅ Challenge management  

## ⚙️ Local Testing Before Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="sqlite:///app.db"
export GOOGLE_API_KEY="your_key"
export SECRET_KEY="dev_secret"

# Run locally
python -m app.run
```

Access at `http://localhost:5000`

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check requirements.txt and Dockerfile syntax |
| Database error | Verify DATABASE_URL is correct and accessible |
| Email not sending | Confirm SMTP credentials and use app password for Gmail |
| Port error | HF Spaces uses port 7860 (already configured) |

## 📖 Resources

- [HF Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 📝 Notes

- Change hardcoded `SECRET_KEY` in `app.run` to use environment variable
- Ensure database is accessible from HF's servers
- Monitor logs for any runtime errors
- Start with CPU hardware, upgrade if needed

---

**Ready to deploy? Push to your HF Space repo and watch it build!** 🎯
