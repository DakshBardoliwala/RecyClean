import cv2
import speech_recognition as sr
import requests
from PIL import Image
import io
import tempfile
import os
import time
from gtts import gTTS
from playsound import playsound
from examples import examples

# Hugging Face API details
HF_API_TOKEN = ""
HF_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

# ChatGPT API details
CHATGPT_API_URL = "https://api.openai.com/v1/chat/completions"
CHATGPT_API_KEY = ""

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

def chatgpt_analysis(caption):
    """
    Use ChatGPT to analyze the caption and determine if the object is recyclable.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CHATGPT_API_KEY}"
        }

        # More detailed prompt providing background knowledge
        refined_prompt = (
            "You are an expert in recycling guidelines across different municipalities. You have deep knowledge of:\n"
            "- Commonly recyclable materials (e.g., plastic #1 and #2, glass, aluminum, cardboard)\n"
            "- Special considerations for electronic waste (e.g., laptops, phones) which are recyclable in specialized facilities\n"
            "- Items commonly not accepted by curbside programs (e.g., certain plastics #3-#7, heavily contaminated items)\n"
            "- Local variations in recycling rules\n\n"
            "When you receive a description of an item, you should base your assessment on general, widely accepted recycling practices.\n"
            "If the item is clearly a commonly recycled material or device, respond with 'This item is recyclable.'\n"
            "If the item is clearly not accepted in typical recycling streams, respond with 'This item is not recyclable.'\n"
            "If it's unclear (e.g., the plastic type isn’t known or it’s contaminated), respond with 'I am not sure if this item is recyclable.'\n\n"
            "Answer ONLY with one of the following:\n"
            "1. 'This item is recyclable.'\n"
            "2. 'This item is not recyclable.'\n"
            "3. 'I am not sure if this item is recyclable.'\n\n"
            "Do not provide additional commentary or reasoning in your final answer—just choose one of the three sentences.\n"
            "Here are some detailed examples of items and the reasoning behind each:\n\n"
            f"{examples}"
            "Now, here is the description of an object to analyze:\n\n"
            f"{caption}\n\n"
            "Review the item carefully and decide which of the three statements best fits.\n"
            "Remember: Only return one of the three statements as your final answer."
        )

        data = {
            # Use "gpt-4" if you have access; otherwise "gpt-3.5-turbo"
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful, factual assistant."},
                {"role": "user", "content": refined_prompt}
            ]
        }

        response = requests.post(CHATGPT_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            return reply.strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error contacting ChatGPT: {str(e)}"



def generate_caption(image_path):
    """
    Generate a detailed multi-sentence caption for the given image using the Hugging Face API.
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            
            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

        # Send request to Hugging Face API with raw bytes
        response = requests.post(
            HF_API_URL,
            headers=headers,
            data=img_byte_arr
        )

        if response.status_code == 200:
            initial_caption = response.json()[0]["generated_text"]
            return initial_caption
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error processing image: {str(e)}"

def capture_single_description():
    """
    Capture a single frame, describe it, determine recyclability, and close the camera.
    """
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    try:
        # Wait a moment for camera to initialize
        time.sleep(1)
        
        # Show webcam feed until we get a good frame
        for _ in range(10):  # Try up to 10 frames
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Webcam Feed', frame)
                cv2.waitKey(1)
                break
        
        if not ret:
            print("Error: Could not read frame")
            return
        
        # Create temporary file for the image with unique name
        temp_dir = tempfile.gettempdir()
        temp_image = os.path.join(temp_dir, f'frame_{time.time()}.jpg')
        
        try:
            # Save the frame
            cv2.imwrite(temp_image, frame)
            
            # Generate and print caption
            caption = generate_caption(temp_image)
            print("\nCaption:", caption)
            
            # Use ChatGPT to analyze recyclability
            recyclability_response = chatgpt_analysis(caption)
            print("\nChatGPT Response:", recyclability_response)
            
            # Speak the response
            speak_text(recyclability_response)
            
        finally:
            # Clean up image file
            try:
                os.remove(temp_image)
            except:
                pass  # If we can't delete now, it'll be cleaned up later
                
    finally:
        # Always clean up camera resources
        cap.release()
        cv2.destroyAllWindows()
def listen_for_command():
    """
    Listen for the 'describe' command using speech recognition.
    """
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening for 'describe' command...")
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            # Listen for audio input with a timeout
            audio = recognizer.listen(source, timeout=5)
            # Convert audio to text using Google Speech Recognition
            text = recognizer.recognize_google(audio).lower()
            # Check if the command "describe" is in the recognized text
            return "describe" in text
        except sr.WaitTimeoutError:
            # Handle case where no input was received within timeout
            return False
        except sr.UnknownValueError:
            # Handle case where speech was unintelligible
            return False
        except sr.RequestError:
            # Handle API errors from the speech recognition service
            print("Could not request results from speech recognition service")
            return False

def main_loop():
    """
    Main program loop that listens for commands and handles camera cycling.
    """
    print("Starting webcam descriptor...")
    print("Say 'describe' to capture and describe a frame")
    print("Press Ctrl+C to quit")
    
    try:
        while True:
            # Listen for command
            if listen_for_command():
                print("Command detected! Opening camera...")
                capture_single_description()
                print("\nCamera closed. Listening for next command...")
            
    except KeyboardInterrupt:
        print("\nExiting program...")

if __name__ == "__main__":
    main_loop()
