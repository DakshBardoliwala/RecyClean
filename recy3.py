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
            playsound(temp_filename)
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

        # Expanded examples with more detail
        examples = (
            "Examples:\n"
"1) Description: 'A #1 plastic water bottle with a recycling symbol.' -> This item is recyclable.\n"
"   Reasoning: Plastic #1 is commonly accepted in most curbside recycling programs.\n\n"
"2) Description: 'A Styrofoam takeout container (#6).' -> This item is not recyclable.\n"
"   Reasoning: Polystyrene foam is typically not accepted by standard curbside recycling.\n\n"
"3) Description: 'A piece of plastic wrap of unknown type.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Without a clear recycling code, many programs do not accept it.\n\n"
"4) Description: 'A man holding a laptop (metal and plastic parts).' -> This item is recyclable.\n"
"   Reasoning: Electronics can be recycled through special e-waste facilities.\n\n"
"5) Description: 'A mobile phone.' -> This item is recyclable.\n"
"   Reasoning: Phones are e-waste with recoverable metals and plastics.\n\n"
"6) Description: 'A greasy cardboard pizza box.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Heavily soiled cardboard is often rejected by curbside programs.\n\n"
"7) Description: 'A plastic bottle without a label or number marking.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Unmarked plastic is questionable for many facilities.\n\n"
"8) Description: 'An empty aluminum soda can.' -> This item is recyclable.\n"
"   Reasoning: Aluminum is widely accepted in recycling.\n\n"
"9) Description: 'A glass jar with a metal lid.' -> This item is recyclable.\n"
"   Reasoning: Both glass and metal lids are commonly accepted, though they may need to be separated.\n\n"
"10) Description: 'A plastic toy (unknown plastic type).' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Toys often use mixed or unknown plastics not accepted by curbside programs.\n\n"
"11) Description: 'A hardcover book.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Some facilities accept books if covers are removed, others do not.\n\n"
"12) Description: 'An empty steel soup can.' -> This item is recyclable.\n"
"   Reasoning: Steel cans are commonly accepted curbside.\n\n"
"13) Description: 'A bubble mailer made of mixed plastic and paper.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Mixed materials can be problematic unless separated.\n\n"
"14) Description: 'A cardboard shipping box (clean and dry).' -> This item is recyclable.\n"
"   Reasoning: Clean cardboard is almost universally accepted.\n\n"
"15) Description: 'A plastic fork labeled #5.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: #5 plastics are sometimes accepted, but rules vary by location.\n\n"
"16) Description: 'A #2 HDPE milk jug.' -> This item is recyclable.\n"
"   Reasoning: Plastic #2 is widely accepted.\n\n"
"17) Description: 'Plastic straws (no recycling mark).' -> This item is not recyclable.\n"
"   Reasoning: Most straws are too small or made from mixed plastics, typically not recycled.\n\n"
"18) Description: 'A wet paper towel.' -> This item is not recyclable.\n"
"   Reasoning: Wet or soiled paper cannot be recycled.\n\n"
"19) Description: 'A metal coat hanger.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Some facilities accept metal hangers, but many ask for them to be taken to special drop-offs.\n\n"
"20) Description: 'A shredded stack of office paper.' -> This item is recyclable.\n"
"   Reasoning: Shredded paper can be recycled in some programs if properly contained.\n\n"
"21) Description: 'A plastic coffee cup lid labeled #6.' -> This item is not recyclable.\n"
"   Reasoning: Polystyrene (#6) lids are usually not accepted.\n\n"
"22) Description: 'Used paper napkins.' -> This item is not recyclable.\n"
"   Reasoning: Soiled paper fiber is rejected.\n\n"
"23) Description: 'An empty glass wine bottle.' -> This item is recyclable.\n"
"   Reasoning: Glass bottles are commonly accepted curbside.\n\n"
"24) Description: 'A phone charger and cable.' -> This item is recyclable.\n"
"   Reasoning: Electronic accessories can be taken to e-waste facilities.\n\n"
"25) Description: 'A plastic grocery bag labeled #4 (LDPE).' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Some stores offer special drop-offs for bags, but curbside often rejects them.\n\n"
"26) Description: 'A PET #1 clear clamshell container (for salad).' -> This item is recyclable.\n"
"   Reasoning: PET #1 is generally accepted if clean.\n\n"
"27) Description: 'A ceramic coffee mug.' -> This item is not recyclable.\n"
"   Reasoning: Ceramics are not accepted in standard glass recycling.\n\n"
"28) Description: 'A plastic laundry detergent jug labeled #2.' -> This item is recyclable.\n"
"   Reasoning: HDPE #2 jugs are commonly accepted.\n\n"
"29) Description: 'A single-use plastic ketchup packet.' -> This item is not recyclable.\n"
"   Reasoning: Small flexible packets are not typically accepted.\n\n"
"30) Description: 'A tissue box (cardboard with plastic film opening).' -> I am not sure if this item is recyclable.\n"
"   Reasoning: The cardboard is recyclable, but the plastic film must usually be removed first.\n\n"
"31) Description: 'A cork from a wine bottle.' -> This item is not recyclable.\n"
"   Reasoning: Natural cork isn’t commonly accepted in curbside recycling.\n\n"
"32) Description: 'A #5 plastic yogurt cup.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Some communities accept #5 plastic, others do not.\n\n"
"33) Description: 'A partially filled paint can.' -> This item is not recyclable.\n"
"   Reasoning: Hazardous or chemical residues generally require special disposal.\n\n"
"34) Description: 'A rinsed-out tin can with a label.' -> This item is recyclable.\n"
"   Reasoning: Tin or steel cans are widely accepted, labels can typically be removed or left on.\n\n"
"35) Description: 'A broken Pyrex baking dish.' -> This item is not recyclable.\n"
"   Reasoning: Heat-treated glass (Pyrex) is not compatible with standard glass recycling.\n\n"
"36) Description: 'A #7 mixed plastic container.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: #7 often indicates a mix of plastics that some centers do not accept.\n\n"
"37) Description: 'A cotton t-shirt.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Textiles are not typically accepted curbside, but can be recycled through textile recycling programs.\n\n"
"38) Description: 'A cardboard egg carton.' -> This item is recyclable.\n"
"   Reasoning: Cardboard or paper egg cartons are usually accepted if clean.\n\n"
"39) Description: 'A used tea bag (paper with tea leaves).' -> This item is not recyclable.\n"
"   Reasoning: Organic material contamination and staples can be problematic.\n\n"
"40) Description: 'Empty aerosol can (non-hazardous).' -> This item is recyclable.\n"
"   Reasoning: Some facilities accept empty aerosol cans if fully depressurized.\n\n"
"41) Description: 'Used aluminum foil covered in food residue.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Foil must be clean to be accepted; heavily soiled foil is typically rejected.\n\n"
"42) Description: 'A broken mirror.' -> This item is not recyclable.\n"
"   Reasoning: Mirrors are treated glass and not accepted with standard glass recycling.\n\n"
"43) Description: 'A plastic takeout container labeled #5.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Some places accept #5 clamshells, others do not.\n\n"
"44) Description: 'A cereal box (paperboard) with inner plastic bag.' -> This item is recyclable.\n"
"   Reasoning: The box is recyclable; the liner is not, unless taken to specific drop-offs.\n\n"
"45) Description: 'A plastic sauce bottle labeled #1.' -> This item is recyclable.\n"
"   Reasoning: Clean PET #1 plastic is widely accepted.\n\n"
"46) Description: 'A plastic toy with metal screws inside.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Mixed materials require special handling.\n\n"
"47) Description: 'A cast iron pan.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Metal is recyclable, but curbside pickup may not accept heavy cookware.\n\n"
"48) Description: 'A toothpaste tube (mixed materials).' -> This item is not recyclable.\n"
"   Reasoning: Most toothpaste tubes use multi-layer plastics or metal.\n\n"
"49) Description: 'A cardboard coffee cup sleeve (clean).' -> This item is recyclable.\n"
"   Reasoning: Plain cardboard is generally accepted.\n\n"
"50) Description: 'A small LED light bulb.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Some e-waste facilities accept them, but not regular curbside.\n\n"
"51) Description: 'A porcelain plate.' -> This item is not recyclable.\n"
"   Reasoning: Ceramics are generally not accepted curbside.\n\n"
"52) Description: 'Paper envelopes with plastic windows.' -> This item is recyclable.\n"
"   Reasoning: Many recycling systems accept envelopes with small plastic windows.\n\n"
"53) Description: 'A used disposable diaper.' -> This item is not recyclable.\n"
"   Reasoning: Diapers contain waste and mixed materials, never accepted.\n\n"
"54) Description: 'A big cardboard moving box (flattened).' -> This item is recyclable.\n"
"   Reasoning: Clean, flattened cardboard is standard in recycling.\n\n"
"55) Description: 'A chip bag made of foil-lined plastic.' -> This item is not recyclable.\n"
"   Reasoning: Mixed materials are difficult to separate and typically not accepted.\n\n"
"56) Description: 'A used plastic cup labeled #1 (clean).' -> This item is recyclable.\n"
"   Reasoning: Clean PET cups are generally accepted.\n\n"
"57) Description: 'A broken PVC pipe (#3 plastic).' -> This item is not recyclable.\n"
"   Reasoning: PVC is rarely accepted in curbside recycling.\n\n"
"58) Description: 'A piece of bubble wrap.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Some drop-off locations accept bubble wrap, but curbside often rejects it.\n\n"
"59) Description: 'An empty clear glass pasta sauce jar.' -> This item is recyclable.\n"
"   Reasoning: Clear glass jars are generally accepted.\n\n"
"60) Description: 'A roll of used fax paper (thermal paper).' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Thermal paper may contain chemicals that some facilities do not accept.\n\n"
"61) Description: 'A shredded plastic bag used as packing material.' -> This item is not recyclable.\n"
"   Reasoning: Plastic film and shredded pieces can jam sorting machines.\n\n"
"62) Description: 'A plastic laundry basket with no recycling label.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Large plastic items without labels are often not accepted.\n\n"
"63) Description: 'A metal soda bottle cap.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Tiny metal caps can be recycled in some programs if placed inside larger metal cans.\n\n"
"64) Description: 'A completely empty and clean paint can (metal).' -> This item is recyclable.\n"
"   Reasoning: If thoroughly cleaned, some facilities accept metal paint cans.\n\n"
"65) Description: 'A polypropylene (#5) medicine bottle (empty).' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Depends on local rules; some accept #5 containers, others do not.\n\n"
"66) Description: 'A foam egg carton labeled #6.' -> This item is not recyclable.\n"
"   Reasoning: Styrofoam (#6) is typically rejected.\n\n"
"67) Description: 'A used bandage with adhesive and gauze.' -> This item is not recyclable.\n"
"   Reasoning: Medical waste or soiled materials are not accepted.\n\n"
"68) Description: 'A cardboard cereal box with minor grease spots.' -> This item is recyclable.\n"
"   Reasoning: Light grease typically won’t disqualify dry cardboard.\n\n"
"69) Description: 'A photograph printed on glossy photo paper.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Photo paper may have chemical coatings that are not recyclable.\n\n"
"70) Description: 'A large plastic tote labeled #2 HDPE.' -> This item is recyclable.\n"
"   Reasoning: If it fits, many programs accept rigid #2 plastics, but size rules may vary.\n\n"
"71) Description: 'A combination shampoo/conditioner bottle labeled #2 and #5.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Mixed plastic components can complicate recycling.\n\n"
"72) Description: 'An empty juice box with a plastic straw attached.' -> This item is not recyclable.\n"
"   Reasoning: Juice boxes are often multi-layer cartons, and the straw is plastic.\n\n"
"73) Description: 'A tin foil pie plate cleaned of food residue.' -> This item is recyclable.\n"
"   Reasoning: Clean aluminum foil products are often accepted.\n\n"
"74) Description: 'A foil-like gift wrap paper with glitter.' -> This item is not recyclable.\n"
"   Reasoning: Glitter and mixed materials make it unsuitable for paper recycling.\n\n"
"75) Description: 'A nylon bag used to hold fruit (netting).' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Netting is often not accepted curbside.\n\n"
"76) Description: 'A polylactic acid (PLA) compostable cup.' -> This item is not recyclable.\n"
"   Reasoning: Compostable plastics do not break down in traditional recycling.\n\n"
"77) Description: 'A plastic clamshell labeled #1 (for berries).' -> This item is recyclable.\n"
"   Reasoning: Many municipalities accept clean #1 containers.\n\n"
"78) Description: 'A used brown paper lunch bag (slightly stained).' -> I am not sure if this item is recyclable.\n"
"   Reasoning: If lightly stained, it might still be accepted, but heavily soiled bags are not.\n\n"
"79) Description: 'A small cardboard jewelry box with a foam insert.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: The cardboard is recyclable, but the foam insert is not.\n\n"
"80) Description: 'A used paper cup with a wax lining.' -> This item is not recyclable.\n"
"   Reasoning: Most waxed or plastic-lined paper cups are not accepted curbside.\n\n"
"81) Description: 'A broken plastic chair labeled #5.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Large rigid plastics may be accepted in some areas, but not all.\n\n"
"82) Description: 'A single-use coffee pod (plastic + aluminum foil).' -> This item is not recyclable.\n"
"   Reasoning: Pods are typically mixed materials and difficult to separate.\n\n"
"83) Description: 'A sealed, unopened can of expired food.' -> This item is not recyclable.\n"
"   Reasoning: Food liquids and sealed pressurized cans are usually not accepted.\n\n"
"84) Description: 'A paper-based mailing envelope lined with bubble wrap.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Mixed paper and plastic must be separated, which is often difficult.\n\n"
"85) Description: 'A PET #1 shampoo bottle (rinsed).' -> This item is recyclable.\n"
"   Reasoning: Clean PET #1 bottles are widely accepted.\n\n"
"86) Description: 'A PVC pipe labeled #3 used for plumbing.' -> This item is not recyclable.\n"
"   Reasoning: PVC #3 is rarely accepted in curbside recycling.\n\n"
"87) Description: 'A stack of newspapers (dry and unsoiled).' -> This item is recyclable.\n"
"   Reasoning: Clean newspapers are standard in paper recycling.\n\n"
"88) Description: 'A used plastic straw wrapper with some food stains.' -> This item is not recyclable.\n"
"   Reasoning: Thin plastic film with food residue is generally rejected.\n\n"
"89) Description: 'A broken porcelain vase.' -> This item is not recyclable.\n"
"   Reasoning: Ceramics cannot go with regular glass.\n\n"
"90) Description: 'A large cardboard tube from gift wrap.' -> This item is recyclable.\n"
"   Reasoning: Plain cardboard or paper tubes are generally accepted.\n\n"
"91) Description: 'A snack-size yogurt tube (soft plastic).' -> This item is not recyclable.\n"
"   Reasoning: Squeezable tubes made of multilayer plastic are typically not accepted.\n\n"
"92) Description: 'A polypropylene (#5) Tupperware container.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Some programs accept #5 containers, others do not.\n\n"
"93) Description: 'A beverage carton for milk (paper + plastic lining).' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Many facilities do accept these cartons, but rules vary.\n\n"
"94) Description: 'A used coffee filter with grounds.' -> This item is not recyclable.\n"
"   Reasoning: Compostable, but not acceptable for curbside recycling.\n\n"
"95) Description: 'A plastic container labeled #4 LDPE for bread.' -> I am not sure if this item is recyclable.\n"
"   Reasoning: Some curbside programs do not accept #4 containers or films.\n\n"
"96) Description: 'An old DVD disc.' -> This item is not recyclable.\n"
"   Reasoning: Discs are mixed materials (polycarbonate, metals) and require special e-waste handling.\n\n"
"97) Description: 'A clean, empty peanut butter jar (#1 plastic).' -> This item is recyclable.\n"
"   Reasoning: Plastic #1 is commonly accepted if thoroughly rinsed.\n\n"
"98) Description: 'A used paper plate with heavy food residue.' -> This item is not recyclable.\n"
"   Reasoning: Heavily soiled paper is not accepted.\n\n"
"99) Description: 'A latex glove.' -> This item is not recyclable.\n"
"   Reasoning: Gloves are not accepted in typical curbside recycling.\n\n"
"100) Description: 'A large aluminum tray (clean).' -> This item is recyclable.\n"
"    Reasoning: Clean aluminum trays are accepted in many curbside programs.\n\n"

        )

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
