import cv2
import speech_recognition as sr
import requests
from PIL import Image
import io
import tempfile
import os
import time
import openai
from SpeakText import speak_text

# Hugging Face API details
API_TOKEN = ""
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}


def expand_caption(caption):
    return caption
    """
    Expand a single sentence caption into multiple sentences without using NLTK.
    """
    if '.' in caption[:-1]:
        return caption
    
    descriptive_additions = [
        " The scene is captured with clear detail.",
        " The image shows this in great detail.",
        " This view provides additional context to the scene.",
        " The composition effectively captures the subject."
    ]
    from random import choice
    return caption + choice(descriptive_additions)

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

        # Send request to API with raw bytes
        response = requests.post(
            API_URL,
            headers=headers,
            data=img_byte_arr
        )

        if response.status_code == 200:
            initial_caption = response.json()[0]["generated_text"]
            detailed_caption = expand_caption(initial_caption)
            return detailed_caption
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error processing image: {str(e)}"

def listen_for_command():
    """
    Listen for the 'describe' command using speech recognition.
    """
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening for 'describe' command...")
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio).lower()
            return "describe" in text
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except sr.RequestError:
            print("Could not request results from speech recognition service")
            return False

def capture_single_description():
    """
    Capture a single frame, describe it, and close the camera
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
            print("\nDescription:", caption)
            
            # Speak the caption
            speak_text(caption)
            
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


def chatgpt_explain_labels(labels):
    """Uses ChatGPT to classify a detected object."""
    if not labels:
        return "No label detected."
    prompt = (f"Classify this object, {labels[0]}, as one of the following waste categories. "
              "Choose the one that fits best, do not assume anything about the context:\n"
              "Recycling\nOrganic\nTrash\nElectronic\nMiscellaneous\n\n"
              "Give your response as only one word: the category.")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a classification system for waste categories."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0
    )
    return response.choices[0].message['content'].strip()


def main_loop():
    """
    Main program loop that listens for commands and handles camera cycling
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