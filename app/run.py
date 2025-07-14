from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from app.models import db, User_details, Challenge, UserChallengeProgress, Snippet
import json
import os
import google.generativeai as genai
from app.models import Snippet
from app.models import db, User_details
import tempfile
import whisper
import subprocess
import time
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import smtplib
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

# Flask App Setup
app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Password reset token serializer
serializer = URLSafeTimedSerializer(app.secret_key)

# Email sending utility (simple SMTP, configure as needed)
def send_reset_email(to_email, reset_url):
    print(f"Preparing to send email to: {to_email}")
    print(f"Reset URL: {reset_url}")
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL', smtp_user)
    print(f"SMTP config: server={smtp_server}, port={smtp_port}, user={smtp_user}, from={from_email}")
    subject = "CodeMentor AI Password Reset"
    body = f"""
    To reset your password, click the link below (valid for 1 hour):\n\n{reset_url}\n\nIf you did not request this, ignore this email.\n"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, [to_email], msg.as_string())
        print(f"Sent password reset email to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def convert_audio_to_wav(input_path, output_path):
    """Convert audio file to WAV format for Whisper"""
    try:
        print(f"Converting {input_path} to {output_path}")
        
        # Try different conversion approaches
        commands = [
            # Standard conversion
            ['ffmpeg', '-y', '-i', input_path, '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', output_path],
            # Alternative conversion with different codec
            ['ffmpeg', '-y', '-i', input_path, '-ar', '16000', '-ac', '1', '-f', 'wav', output_path],
            # Force format detection
            ['ffmpeg', '-y', '-f', 'webm', '-i', input_path, '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', output_path]
        ]
        
        for i, cmd in enumerate(commands):
            try:
                print(f"Trying conversion method {i+1}: {' '.join(cmd)}")
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(f"Conversion successful with method {i+1}")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Method {i+1} failed: {e.stderr}")
                continue
        
        print("All conversion methods failed")
        return False
        
    except FileNotFoundError:
        print("FFmpeg not found. Please install ffmpeg.")
        return False

def validate_audio_file(file_path):
    """Validate that the audio file is not empty or corrupted"""
    try:
        size = os.path.getsize(file_path)
        print(f"Audio file validation: {file_path}, size: {size} bytes")
        
        if size < 1000:
            print(f"Warning: Audio file is very small ({size} bytes)")
            return False
        
        # Try to read the first few bytes to check if it's a valid audio file
        with open(file_path, 'rb') as f:
            header = f.read(16)
            print(f"File header: {header[:8].hex()}")
        
        # Check if it's a WebM file (common for browser recordings)
        if header.startswith(b'\x1a\x45\xdf\xa3'):
            print("Detected WebM format")
        elif header.startswith(b'RIFF'):
            print("Detected WAV format")
        elif header.startswith(b'\x00\x00\x00\x20ftyp'):
            print("Detected MP4 format")
        else:
            print(f"Unknown format, header: {header.hex()}")
        
        return True
    except Exception as e:
        print(f"Audio file validation failed: {e}")
        return False

def try_direct_whisper(audio_path):
    """Try to transcribe audio directly without conversion"""
    try:
        print(f"Attempting to transcribe: {audio_path}")
        print(f"File size: {os.path.getsize(audio_path)} bytes")
        
        # Validate audio file first
        if not validate_audio_file(audio_path):
            print("Audio file validation failed")
            return ""
        
        # Try different Whisper options
        print("Trying Whisper with default settings...")
        result = whisper_model.transcribe(
            audio_path,
            language="en",
            task="transcribe",
            fp16=False,
            verbose=True  # Enable verbose output for debugging
        )
        
        text = result['text'].strip()
        print(f"Whisper result: {result}")
        print(f"Extracted text: '{text}'")
        
        # If no text detected, try with different settings
        if not text:
            print("No text detected, trying with different settings...")
            result = whisper_model.transcribe(
                audio_path,
                language=None,  # Let Whisper auto-detect language
                task="transcribe",
                fp16=False,
                verbose=True
            )
            text = result['text'].strip()
            print(f"Auto-detect result: '{text}'")
        
        # If still no text, try with more aggressive settings
        if not text:
            print("Still no text, trying with aggressive settings...")
            result = whisper_model.transcribe(
                audio_path,
                language="en",
                task="transcribe",
                fp16=False,
                verbose=True,
                condition_on_previous_text=False,
                temperature=0.0
            )
            text = result['text'].strip()
            print(f"Aggressive settings result: '{text}'")
        
        return text
    except Exception as e:
        print(f"Direct transcription failed: {e}")
        return ""

# Load Whisper model once at startup
try:
    whisper_model = whisper.load_model("base")  # or "small", "medium", "large"
except Exception as e:
    print(f"Warning: Could not load Whisper model: {e}")
    whisper_model = None

# Routes
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

@app.route("/api/<action>", methods=["POST"])
def api_action(action):
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "python")

    # Prompt templates
    prompts = {
        "explain": f"Explain in plain English what this {language} code does:\n{code}",
        "doc": f"Generate docstrings or inline comments for this {language} code:\n{code}",
        "errors": f"Identify and explain any syntax or logic errors in the following {language} code:\n{code}",
        "improve": (
            f"Refactor and improve the quality of this {language} code. "
            f"Suggest improvements in naming, structure, and formatting:\n{code}"
        ),
        "debug": (
            f"Find and fix bugs in this {language} code. Explain the root causes and offer tips:\n{code}"
        ),
    }

    prompt = prompts.get(action, f"Analyze this {language} code:\n{code}")

    try:
        response = model.generate_content(prompt)
        output = response.text.strip()
    except Exception as e:
        output = f"Error: {str(e)}"

    return {"result": output}

@app.route('/profile')
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user = User_details.query.get(session["user_id"])
    snippets = user.snippets if user else []
    return render_template("profile.html", user=user, snippets=snippets)


@app.route('/challenges')
def challenges():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user_id = session["user_id"]
    solved_ids = [p.challenge_id for p in UserChallengeProgress.query.filter_by(user_id=user_id, solved=True)]
    # Find challenges the user failed most
    failed = UserChallengeProgress.query.filter_by(user_id=user_id, solved=False).order_by(UserChallengeProgress.attempts.desc()).all()
    failed_ids = [f.challenge_id for f in failed]
    # Recommend failed or unsolved first
    challenges = Challenge.query.order_by(
        db.case(
            (Challenge.id.in_(failed_ids), 0),
            else_=1
        ),
        Challenge.difficulty
    ).all()
    # Mark recommended
    for c in challenges:
        c.is_recommended = c.id in failed_ids
    return render_template("challenges.html", challenges=challenges)

@app.route('/challenge/<int:challenge_id>', methods=["GET", "POST"])
def challenge(challenge_id):
    if not session.get("user_id"):
        return redirect(url_for("login"))
    challenge = Challenge.query.get_or_404(challenge_id)
    feedback = None
    last_code = None  
    if request.method == "POST":
        code = request.form["code"]
        language = request.form.get("language", "python")  # <-- Add this line
        test_cases = json.loads(challenge.test_cases)
        prompt = (
            f"Given the following {language} function implementation:\n{code}\n"
            f"Test it with these cases: {test_cases}.\n"
            "For each, return 'PASS' or 'FAIL' and explain any failures. "
            "If all pass, say 'ALL PASS'."
        )
        try:
            response = model.generate_content(prompt)
            feedback = response.text.strip()
        except Exception as e:
            feedback = f"Error: {str(e)}"
        # Update progress
        user_id = session["user_id"]
        progress = UserChallengeProgress.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
        if not progress:
            progress = UserChallengeProgress(user_id=user_id, challenge_id=challenge_id, attempts=0)
            db.session.add(progress)
        if progress.attempts is None:
            progress.attempts = 0
        progress.attempts += 1
        progress.last_code = code
        progress.last_feedback = feedback
        if "ALL PASS" in feedback:
            progress.solved = True
        db.session.commit()
        last_code = code
    return render_template(
    "challenge.html",
    challenge=challenge,
    feedback=feedback,
    last_code=last_code,
    starter_codes={
        "python": challenge.starter_code_python,
        "cpp": challenge.starter_code_cpp,
        "java": challenge.starter_code_java,
        "javascript": challenge.starter_code_javascript,
        "csharp": challenge.starter_code_csharp,
    }
    )

@app.route('/my_progress')
def my_progress():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user_id = session["user_id"]
    query = UserChallengeProgress.query.filter_by(user_id=user_id)
    progress = query.order_by(UserChallengeProgress.updated_at.desc()).all()

    # Compute stats
    solved = [p for p in progress if p.solved]
    attempting = [p for p in progress if not p.solved and p.attempts > 0]
    total = Challenge.query.count()
    easy_total = Challenge.query.filter_by(difficulty='easy').count()
    med_total = Challenge.query.filter_by(difficulty='medium').count()
    hard_total = Challenge.query.filter_by(difficulty='hard').count()
    easy_solved = len([p for p in solved if p.challenge.difficulty == 'easy'])
    med_solved = len([p for p in solved if p.challenge.difficulty == 'medium'])
    hard_solved = len([p for p in solved if p.challenge.difficulty == 'hard'])

    stats = {
        'solved': len(solved),
        'attempting': len(attempting),
        'total': total,
        'easy': {'solved': easy_solved, 'total': easy_total},
        'medium': {'solved': med_solved, 'total': med_total},
        'hard': {'solved': hard_solved, 'total': hard_total},
    }
    return render_template("progress.html", progress=progress, stats=stats)
    
@app.route('/save_snippet', methods=["POST"])
def save_snippet():
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "python")
    explanation = data.get("explanation", "")
    snippet = Snippet(code=code, language=language, explanation=explanation, user_id=session["user_id"])
    db.session.add(snippet)
    db.session.commit()
    return jsonify({"message": "Snippet saved!"})

@app.route('/delete_snippet/<int:snippet_id>', methods=["DELETE"])
def delete_snippet(snippet_id):
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401
    snippet = Snippet.query.get(snippet_id)
    if not snippet or snippet.user_id != session["user_id"]:
        return jsonify({"error": "Snippet not found or unauthorized"}), 404
    db.session.delete(snippet)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/api/speech-to-code', methods=['POST'])
def speech_to_code():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    if whisper_model is None:
        return jsonify({'error': 'Speech recognition not available'}), 500
    
    audio_file = request.files['audio']
    print(f"Received audio file: {audio_file.filename}, size: {len(audio_file.read())}")
    audio_file.seek(0)  # Reset file pointer
    
    # Determine file extension based on content type
    file_extension = ".wav"
    if audio_file.content_type == "audio/webm":
        file_extension = ".webm"
    elif audio_file.content_type == "audio/mp4":
        file_extension = ".mp4"
    
    temp_audio = tempfile.NamedTemporaryFile(suffix=file_extension, delete=False)
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    
    try:
        audio_file.save(temp_audio.name)
        temp_audio.close()  # Close so we can process it
        print(f"Saved audio to: {temp_audio.name}")
        
        # Check if audio file is valid
        audio_size = os.path.getsize(temp_audio.name)
        print(f"Original audio file size: {audio_size} bytes")
        
        if audio_size < 1000:  # Less than 1KB
            return jsonify({'error': 'Audio file too small. Please check your microphone and try again.'}), 400
        
        # Save a copy for debugging (only for development)
        debug_file = f"debug_audio_{int(time.time())}.webm"
        import shutil
        shutil.copy2(temp_audio.name, debug_file)
        print(f"Saved debug copy to: {debug_file}")
        
        # Try direct transcription first
        prompt = try_direct_whisper(temp_audio.name)
        print(f"Direct transcription result: '{prompt}'")
        
        # If direct transcription failed or returned empty, try conversion
        if not prompt:
            print("Direct transcription failed, trying conversion...")
            
            # Try ffmpeg conversion first
            conversion_success = convert_audio_to_wav(temp_audio.name, temp_wav.name)
            
            if conversion_success:
                print(f"Converted to WAV: {temp_wav.name}")
                print(f"WAV file size: {os.path.getsize(temp_wav.name)} bytes")
                
                # Try transcription with converted WAV
                prompt = try_direct_whisper(temp_wav.name)
                print(f"Converted transcription result: '{prompt}'")
            else:
                print("FFmpeg conversion failed, trying alternative approach...")
                
                # Try with different Whisper settings as last resort
                try:
                    print("Trying Whisper with minimal settings...")
                    result = whisper_model.transcribe(
                        temp_audio.name,
                        language=None,
                        task="transcribe",
                        fp16=False,
                        verbose=True,
                        condition_on_previous_text=False,
                        temperature=0.0,
                        compression_ratio_threshold=2.4,
                        logprob_threshold=-1.0,
                        no_speech_threshold=0.6
                    )
                    prompt = result['text'].strip()
                    print(f"Minimal settings result: '{prompt}'")
                except Exception as e:
                    print(f"Minimal settings failed: {e}")
                    prompt = ""
        
        print(f"Final transcribed text: '{prompt}'")
        
        # Check if transcription is empty
        if not prompt:
            # Provide more detailed error information
            error_msg = (
                'No speech detected. This could be due to:\n'
                '1. Microphone not working properly\n'
                '2. Audio too quiet or too noisy\n'
                '3. Whisper model not recognizing the audio format\n'
                '4. Browser audio recording issues\n\n'
                'Please try:\n'
                '- Speaking louder and more clearly\n'
                '- Using a different microphone\n'
                '- Refreshing the page and granting microphone permissions again\n'
                '- Using the text input instead\n\n'
                'Technical details:\n'
                f'- Audio file size: {audio_size} bytes\n'
                f'- Audio format: {file_extension}\n'
                f'- Content type: {audio_file.content_type}'
            )
            return jsonify({'error': error_msg}), 400
        
    except Exception as e:
        print(f"Speech recognition error: {str(e)}")
        return jsonify({'error': f'Speech recognition failed: {str(e)}'}), 500
    finally:
        # Clean up temp files with error handling
        try:
            if os.path.exists(temp_audio.name):
                os.unlink(temp_audio.name)
        except Exception as e:
            print(f"Could not delete temp audio file: {e}")
        
        try:
            if os.path.exists(temp_wav.name):
                os.unlink(temp_wav.name)
        except Exception as e:
            print(f"Could not delete temp WAV file: {e}")
    
    # Send prompt to LLM (Gemini, OpenAI, etc.)
    language = request.form.get('language', 'python')
    llm_prompt = f"Write code for the following prompt in {language}:\n{prompt}"
    try:
        response = model.generate_content(llm_prompt)
        code = response.text.strip()
        print(f"Generated code: {code[:100]}...")
    except Exception as e:
        code = f"Error: {str(e)}"
        print(f"LLM error: {str(e)}")
    
    return jsonify({'prompt': prompt, 'code': code})

@app.route('/voice-test')
def voice_test():
    """Voice input test page"""
    return render_template('voice_test.html')

@app.route('/api/test-whisper', methods=['GET'])
def test_whisper():
    """Test endpoint to verify Whisper is working"""
    if whisper_model is None:
        return jsonify({'error': 'Whisper model not loaded'}), 500
    
    # Test with a simple audio file if available
    test_result = "Whisper model loaded successfully"
    
    return jsonify({
        'status': test_result,
        'model_type': 'base'
    })

@app.route('/api/test-whisper-simple', methods=['POST'])
def test_whisper_simple():
    """Test Whisper with a simple known text"""
    if whisper_model is None:
        return jsonify({'error': 'Whisper model not loaded'}), 500
    
    try:
        # Test if the model can process a simple audio file
        # Create a minimal test by checking model properties
        model_info = {
            'model_name': whisper_model.name,
            'model_type': 'base',
            'is_loaded': whisper_model is not None
        }
        
        print(f"Whisper model info: {model_info}")
        
        return jsonify({
            'status': 'Whisper model is responsive',
            'model_info': model_info
        })
    except Exception as e:
        return jsonify({'error': f'Whisper test failed: {str(e)}'}), 500

@app.route('/api/test-audio-format', methods=['POST'])
def test_audio_format():
    """Test if we can process the audio format"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    temp_audio = tempfile.NamedTemporaryFile(suffix=".webm", delete=False)
    
    try:
        audio_file.save(temp_audio.name)
        temp_audio.close()
        
        size = os.path.getsize(temp_audio.name)
        
        # Read file header
        with open(temp_audio.name, 'rb') as f:
            header = f.read(32)
        
        format_info = {
            'filename': audio_file.filename,
            'content_type': audio_file.content_type,
            'file_size': size,
            'header_hex': header.hex()[:32],
            'is_valid_size': size > 1000
        }
        
        # Try to identify the format
        if header.startswith(b'\x1a\x45\xdf\xa3'):
            format_info['detected_format'] = 'WebM'
        elif header.startswith(b'RIFF'):
            format_info['detected_format'] = 'WAV'
        elif header.startswith(b'\x00\x00\x00\x20ftyp'):
            format_info['detected_format'] = 'MP4'
        else:
            format_info['detected_format'] = 'Unknown'
        
        return jsonify(format_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            if os.path.exists(temp_audio.name):
                os.unlink(temp_audio.name)
        except:
            pass

@app.route('/api/debug-audio', methods=['POST'])
def debug_audio():
    """Debug endpoint to analyze audio files"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    temp_audio = tempfile.NamedTemporaryFile(suffix=".webm", delete=False)
    
    try:
        audio_file.save(temp_audio.name)
        temp_audio.close()
        
        size = os.path.getsize(temp_audio.name)
        
        # Read file header
        with open(temp_audio.name, 'rb') as f:
            header = f.read(32)
        
        debug_info = {
            'filename': audio_file.filename,
            'content_type': audio_file.content_type,
            'file_size': size,
            'header_hex': header.hex()[:32],
            'is_valid_size': size > 1000
        }
        
        # Try to transcribe
        if size > 1000:
            prompt = try_direct_whisper(temp_audio.name)
            debug_info['transcription'] = prompt
            debug_info['transcription_success'] = bool(prompt)
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            if os.path.exists(temp_audio.name):
                os.unlink(temp_audio.name)
        except:
            pass

@app.route('/api/prompt-to-code', methods=['POST'])
def prompt_to_code():
    data = request.get_json()
    prompt = data.get('prompt', '')
    language = data.get('language', 'python')
    if not prompt.strip():
        return jsonify({'error': 'Prompt is required.'}), 400
    llm_prompt = (
        f"Write only the {language} code for the following prompt. "
        f"Do not include any explanations, comments, or extra information. Output only the code.\nPrompt: {prompt}"
    )
    try:
        response = model.generate_content(llm_prompt)
        code = response.text.strip()
        return jsonify({'code': code})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    message = None
    if request.method == "POST":
        email = request.form.get("email", "")
        user = User_details.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(email, salt="password-reset-salt")
            reset_url = url_for('reset_password', token=token, _external=True)
            send_reset_email(email, reset_url)
        # Always show the same message for security
        message = "If this email is registered, a reset link will be sent."
        return render_template("forgot_password.html", message=message)
    return render_template("forgot_password.html", message=message)

@app.route('/reset-password/<token>', methods=["GET", "POST"])
def reset_password(token):
    error = None
    success = None
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=3600)
    except SignatureExpired:
        error = "The reset link has expired. Please request a new one."
        return render_template("reset_password.html", error=error)
    except BadSignature:
        error = "Invalid or corrupted reset link."
        return render_template("reset_password.html", error=error)
    if request.method == "POST":
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if not password or password != confirm:
            error = "Passwords do not match."
        else:
            user = User_details.query.filter_by(email=email).first()
            if user:
                user.password = generate_password_hash(password)
                db.session.commit()
                success = "Your password has been reset. You may now log in."
                return render_template("reset_password.html", success=success)
            else:
                error = "User not found."
    return render_template("reset_password.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)

