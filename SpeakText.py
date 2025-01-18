import os
from gtts import gTTS
from playsound import playsound
import tempfile
import time


def speak_text(text):
    """
    Convert text to speech using Google TTS
    """
    try:
        # Generate a unique filename
        temp_dir = tempfile.gettempdir()
        temp_filename = os.path.join(temp_dir, f'speech_{time.time()}.mp3')
        
        # Generate speech
        tts = gTTS(text=text, lang='en', slow=False)
        # Save to temporary file
        tts.save(temp_filename)
        
        try:
            # Play the audio

            print('playing sound using native player')
            try:
                os.system("afplay " + temp_filename)
            except:
                pass
            time.sleep(0.5)
            try:
                playsound(temp_filename)
            except:
                pass
        except Exception as e:
            print(f"Error playing sound: {str(e)}")
        finally:
            # Wait a moment before trying to delete
            time.sleep(0.1)
            try:
                os.remove(temp_filename)
            except:
                pass  # If we can't delete now, it'll be cleaned up later
                
    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")

speak_text("Hello World!!")