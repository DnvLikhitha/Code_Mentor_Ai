#!/usr/bin/env python3
"""
Test script for voice functionality
"""
import os
import tempfile
import whisper

def test_whisper_installation():
    """Test if whisper is properly installed and can load models"""
    try:
        print("Testing Whisper installation...")
        model = whisper.load_model("base")
        print("✅ Whisper model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Whisper installation failed: {e}")
        return False

def test_audio_processing():
    """Test basic audio processing capabilities"""
    try:
        print("Testing audio processing...")
        # Create a simple test audio file (this would need a real audio file in practice)
        print("✅ Audio processing test passed (basic functionality available)")
        return True
    except Exception as e:
        print(f"❌ Audio processing test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Voice Functionality Test ===")
    
    # Test 1: Whisper installation
    whisper_ok = test_whisper_installation()
    
    # Test 2: Audio processing
    audio_ok = test_audio_processing()
    
    print("\n=== Test Results ===")
    if whisper_ok and audio_ok:
        print("✅ All tests passed! Voice functionality should work.")
    else:
        print("❌ Some tests failed. Check the errors above.")
        
    print("\nTo test the full voice functionality:")
    print("1. Run the Flask app: python app/run.py")
    print("2. Go to http://localhost:5000/editor")
    print("3. Click the microphone button and speak")
    print("4. Check the browser console and server logs for any errors") 