from PIL import Image

# Hugging Face API details
API_TOKEN = ""
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

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