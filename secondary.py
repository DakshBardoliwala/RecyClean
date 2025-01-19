import io
from google.cloud import vision
from google.cloud.vision_v1 import types
import cv2
import openai
import os
import json

vision_client = vision.ImageAnnotatorClient.from_service_account_json('key.json')
with open('config.json') as f:
    config = json.load(f)

openai.api_key = config["OPENAI_API_KEY"]

def detect_labels_from_frame(frame):
    """Detects labels using Google Vision API from an OpenCV frame."""
    _, encoded_image = cv2.imencode('.jpg', frame)
    content = encoded_image.tobytes()
    image = vision.Image(content=content)
    response = vision_client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return labels

def chatgpt_explain_labels(labels):
    """Uses ChatGPT to classify a detected object."""
    if not labels:
        return "No label detected."
    prompt = (f"Classify this object, {labels[0]}, as one of the following waste categories. "
              "Choose the one that fits best, do not assume anything about the context:\n"
              "Recycling\nOrganic\nTrash\nElectronic\nMiscellaneous\n\n"
              "Give your response as only one word: the category.")
    
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a classification system for waste categories."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0
    )
    return response.choices[0].message['content'].strip()

def main():
    cap = cv2.VideoCapture(0)  # Open default camera
    print("Press 'q' to quit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Display the video stream
        cv2.imshow('RecyClean - Real-Time Waste Classification', frame)
        
        # Process frame every few seconds to avoid excessive API calls
        if cv2.waitKey(1) & 0xFF == ord('d'):  # Press 'd' to classify current frame
            labels = detect_labels_from_frame(frame)
            print(f"Detected labels: {labels}")
            if labels:
                explanation = chatgpt_explain_labels(labels)
                print("\nChatGPT Explanation:")
                print(explanation)
        
        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()