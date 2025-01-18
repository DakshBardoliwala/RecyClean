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

        # Expanded examples with more detail
        examples = (
             """
            RECYCLABLE (30 examples)
Description: 'An empty aluminum soda can.' -> This item is recyclable.
Reasoning: Aluminum is commonly accepted in most recycling programs.

Description: 'A clean #1 plastic water bottle.' -> This item is recyclable.
Reasoning: Plastic #1 (PET) is widely accepted curbside when rinsed.

Description: 'A flattened cardboard box.' -> This item is recyclable.
Reasoning: Clean cardboard is accepted in almost all paper/cardboard recycling.

Description: 'A rinsed-out glass pasta sauce jar.' -> This item is recyclable.
Reasoning: Most glass jars are curbside-recyclable if clean.

Description: 'A clean steel soup can.' -> This item is recyclable.
Reasoning: Steel or tin cans are generally accepted in metal recycling streams.

Description: 'A #2 HDPE milk jug.' -> This item is recyclable.
Reasoning: HDPE is one of the most commonly accepted plastic types.

Description: 'A newspaper.' -> This item is recyclable.
Reasoning: Newspapers are standard paper recyclables.

Description: 'A magazine without plastic wrapping.' -> This item is recyclable.
Reasoning: Glossy magazines (paper) are usually accepted if free of plastic sleeves.

Description: 'A cardboard egg carton.' -> This item is recyclable.
Reasoning: Most paper-based egg cartons are accepted if clean.

Description: 'A clean aluminum foil sheet (balled up).' -> This item is recyclable.
Reasoning: Aluminum foil can be recycled if free of food residue.

Description: 'A roll of clean, empty paper towel tubes.' -> This item is recyclable.
Reasoning: Cardboard tubes are typically accepted with paper products.

Description: 'A clean plastic soda bottle labeled #1.' -> This item is recyclable.
Reasoning: Clear PET #1 plastic is widely recyclable.

Description: 'A cardboard coffee cup sleeve.' -> This item is recyclable.
Reasoning: Plain cardboard or paper sleeves are generally accepted.

Description: 'A newspaper folded neatly.' -> This item is recyclable.
Reasoning: Newspapers are standard recyclable paper items.

Description: 'An empty cardboard shoe box.' -> This item is recyclable.
Reasoning: Cardboard of any kind is normally accepted if clean.

Description: 'A glass beverage bottle (clear).' -> This item is recyclable.
Reasoning: Clean, unbroken glass bottles are typically accepted.

Description: 'A paper grocery bag (no plastic liner).' -> This item is recyclable.
Reasoning: Pure paper bags are generally accepted in paper/cardboard recycling.

Description: 'A clean plastic takeout container labeled #2.' -> This item is recyclable.
Reasoning: Rigid HDPE #2 containers are accepted by many programs.

Description: 'A cardboard shipping box (clean and dry).' -> This item is recyclable.
Reasoning: Clean cardboard is almost universally accepted.

Description: 'A stack of used, but clean, printer paper.' -> This item is recyclable.
Reasoning: Dry, unsoiled paper is acceptable for recycling.

Description: 'A plastic jar labeled #1 PET.' -> This item is recyclable.
Reasoning: PET plastic is among the most accepted types.

Description: 'An empty cardboard gift box (no decorations).' -> This item is recyclable.
Reasoning: Plain cardboard is accepted, but remove bows/ribbons first.

Description: 'Clean glass candle holders (no wax).' -> This item is recyclable.
Reasoning: If thoroughly cleaned, glass is generally recyclable.

Description: 'Clean aluminum baking trays.' -> This item is recyclable.
Reasoning: Aluminum trays are accepted if free of food residue.

Description: 'A plastic lid labeled #2 (from a container).' -> This item is recyclable.
Reasoning: If your facility accepts #2 lids, they can go with plastics.

Description: 'A #5 plastic tub (if locally accepted).' -> This item is recyclable.
Reasoning: Some areas do accept polypropylene containers.

Description: 'A metal food can with a pull-tab top.' -> This item is recyclable.
Reasoning: Steel or tin-based cans remain recyclable despite pull-tab lids.

Description: 'A soda bottle labeled #1 with cap removed.' -> This item is recyclable.
Reasoning: PET #1 bottles are widely recyclable; caps may be recycled separately if #2 or #5.

Description: 'A clean pie tin labeled as aluminum.' -> This item is recyclable.
Reasoning: Aluminum baking tins are acceptable if free of residue.

Description: 'A #2 plastic detergent bottle, thoroughly rinsed.' -> This item is recyclable.
Reasoning: HDPE #2 bottles are among the most universally accepted plastics.

ORGANIC (30 examples)
Description: 'A banana peel.' -> This item is organic.
Reasoning: Fruit peels break down naturally and are compostable.

Description: 'Coffee grounds.' -> This item is organic.
Reasoning: Used coffee grounds are biodegradable and suitable for compost.

Description: 'Apple cores.' -> This item is organic.
Reasoning: Core and seeds decompose quickly.

Description: 'Orange rinds.' -> This item is organic.
Reasoning: Citrus peels are compostable, though they may take longer to break down.

Description: 'Vegetable scraps (carrot tops, celery ends).' -> This item is organic.
Reasoning: These kitchen scraps are ideal for composting.

Description: 'Eggshells.' -> This item is organic.
Reasoning: Eggshells break down, adding calcium to compost.

Description: 'Tea bags (paper-based, no staples).' -> This item is organic.
Reasoning: Paper tea bags and leaves decompose naturally.

Description: 'Potato peels.' -> This item is organic.
Reasoning: Starchy vegetable scraps decompose well in compost.

Description: 'Leftover salad greens (unseasoned).' -> This item is organic.
Reasoning: Plain vegetable matter is compostable.

Description: 'Bread crust (without mold treatments).' -> This item is organic.
Reasoning: Stale bread is compostable, though it can attract pests if not buried.

Description: 'Corn cobs and husks.' -> This item is organic.
Reasoning: They decompose in compost, though cobs take longer.

Description: 'Leafy yard trimmings (grass clippings, leaves).' -> This item is organic.
Reasoning: These are prime materials for compost piles.

Description: 'Paper napkins (lightly used, no chemical residue).' -> This item is organic.
Reasoning: Slightly soiled paper with food residue is compostable.

Description: 'Paper plates labeled “compostable” (food-soiled).' -> This item is organic.
Reasoning: Compostable paper products decompose if they are specifically made for compost.

Description: 'Paper straws.' -> This item is organic.
Reasoning: Paper straws degrade in compost, unlike plastic ones.

Description: 'Wooden toothpicks.' -> This item is organic.
Reasoning: Small pieces of untreated wood break down in compost.

Description: 'Mushroom stems and scraps.' -> This item is organic.
Reasoning: Fungi decompose quickly in compost.

Description: 'Spoiled fruits (overripe bananas, apples, etc.).' -> This item is organic.
Reasoning: Spoiled produce is fully biodegradable.

Description: 'Herb stems (basil, cilantro).' -> This item is organic.
Reasoning: Herb stems are plant matter suitable for compost.

Description: 'Melon rinds (watermelon, cantaloupe).' -> This item is organic.
Reasoning: Melon rinds break down over time in a compost pile.

Description: 'Peanut shells (unseasoned).' -> This item is organic.
Reasoning: Shells decompose, adding carbon to the compost mix.

Description: 'Avocado skins and pits (pits decompose slowly).' -> This item is organic.
Reasoning: They will eventually break down, though pits may take longer.

Description: 'Paper tissues (used for wiping food spills).' -> This item is organic.
Reasoning: Soiled paper is biodegradable, often composted.

Description: 'Nut shells (e.g., pistachio, walnut), unflavored.' -> This item is organic.
Reasoning: Natural shells are compostable though they can be slow to break down.

Description: 'Pineapple tops and skins.' -> This item is organic.
Reasoning: Fruit scraps decompose, though pineapple cores are fibrous.

Description: 'Wilted lettuce leaves.' -> This item is organic.
Reasoning: Leafy greens are ideal “green” compost material.

Description: 'Flower stems from pruning.' -> This item is organic.
Reasoning: Plant-based trimmings are compostable.

Description: 'Paper tablecloth (unwaxed, food-stained).' -> This item is organic.
Reasoning: If it’s purely paper with no plastic lining, it can decompose.

Description: 'Cooked oatmeal leftovers (no added sugars).' -> This item is organic.
Reasoning: Oatmeal is biodegradable if not mixed with non-compostable additives.

Description: 'Any fruit or vegetable scraps (general kitchen waste).' -> This item is organic.
Reasoning: All produce leftovers are biodegradable in compost conditions.

(Continuing in next message due to length.)

ELECTRONICS (30 examples)
Description: 'A smartphone (Android or iPhone).' -> This item is electronics.
Reasoning: Phones contain circuit boards, metals, and batteries requiring e-waste recycling.

Description: 'A laptop (Windows or Mac).' -> This item is electronics.
Reasoning: Laptops house rechargeable batteries and circuit boards, categorized as e-waste.

Description: 'A desktop computer tower.' -> This item is electronics.
Reasoning: Contains complex circuitry and components that need proper e-waste handling.

Description: 'A tablet (touchscreen device).' -> This item is electronics.
Reasoning: Tablets contain lithium batteries and electronic components.

Description: 'A standalone computer monitor (LCD or LED).' -> This item is electronics.
Reasoning: Monitors have circuit boards and sometimes hazardous materials like mercury in older models.

Description: 'A smartwatch or fitness tracker.' -> This item is electronics.
Reasoning: Wearables contain small batteries and microelectronics.

Description: 'A digital camera (DSLR or point-and-shoot).' -> This item is electronics.
Reasoning: Cameras have sensors, circuit boards, and batteries.

Description: 'A DVD or Blu-ray player.' -> This item is electronics.
Reasoning: Optical disc players have circuit boards and mechanical parts.

Description: 'A streaming media device (like a Roku or Apple TV).' -> This item is electronics.
Reasoning: Contains circuit boards and sometimes a small power supply.

Description: 'A wireless router or modem.' -> This item is electronics.
Reasoning: Routers have circuit boards, antennas, and plastic housing.

Description: 'A gaming console (e.g., PlayStation, Xbox).' -> This item is electronics.
Reasoning: Consoles contain complex circuit boards and power units.

Description: 'A gaming controller or joystick.' -> This item is electronics.
Reasoning: Input devices for consoles/computers with internal electronics.

Description: 'A set of computer speakers.' -> This item is electronics.
Reasoning: Speakers contain wiring, magnets, and often a small amplifier board.

Description: 'Wireless headphones or earbuds.' -> This item is electronics.
Reasoning: Contain rechargeable batteries and wireless circuitry.

Description: 'A VR headset.' -> This item is electronics.
Reasoning: Virtual Reality devices have advanced sensors and displays.

Description: 'A digital thermostat (home HVAC controller).' -> This item is electronics.
Reasoning: Thermostats have LCD displays, sensors, and circuit boards.

Description: 'A smartwatch charging dock.' -> This item is electronics.
Reasoning: Docking stations contain electronic charging circuitry.

Description: 'A power supply unit (PSU) for a desktop PC.' -> This item is electronics.
Reasoning: Converts AC to DC power and contains various electronic parts.

Description: 'An external hard drive (HDD or SSD).' -> This item is electronics.
Reasoning: Storage devices contain circuit boards and data platters or chips.

Description: 'A portable USB flash drive.' -> This item is electronics.
Reasoning: Flash memory devices have circuit boards with NAND chips.

Description: 'A digital photo frame.' -> This item is electronics.
Reasoning: Contains a small LCD screen and memory components.

Description: 'A projector (home theater or business).' -> This item is electronics.
Reasoning: Projectors use lamps or LEDs, plus circuit boards for video processing.

Description: 'A portable power bank.' -> This item is electronics.
Reasoning: Power banks contain lithium-ion batteries and charging circuits.

Description: 'A USB wall plug adapter.' -> This item is electronics.
Reasoning: Adapters have transformers or circuit boards to regulate power output.

Description: 'A drone (consumer-grade, with camera).' -> This item is electronics.
Reasoning: Drones have batteries, sensors, motors, and a flight controller board.

Description: 'A smartwatch or fitness tracker.' -> This item is electronics.
Reasoning: Wearables contain rechargeable batteries and sensors.

Description: 'A digital thermometer (medical or home use).' -> This item is electronics.
Reasoning: Has an LCD display and temperature sensor circuitry.

Description: 'A baby monitor set.' -> This item is electronics.
Reasoning: Audio/video transmitters and receivers contain circuit boards.

Description: 'A robotic vacuum cleaner.' -> This item is electronics.
Reasoning: Uses sensors, motors, and CPUs for navigation.

Description: 'A smart light bulb.' -> This item is electronics.
Reasoning: Contains LED drivers and wireless connectivity modules.

MISCELLANEOUS (30 examples)
Description: 'A human being standing in a room.' -> This item is miscellaneous.
Reasoning: Humans are not typically categorized under recycling, organic waste, or electronics.

Description: 'A plush teddy bear.' -> This item is miscellaneous.
Reasoning: Mixed materials (fabric, stuffing) do not fall neatly under recycling or electronics.

Description: 'A porcelain figurine.' -> This item is miscellaneous.
Reasoning: Porcelain is not recyclable curbside; it’s not organic or electronic.

Description: 'A baseball hat.' -> This item is miscellaneous.
Reasoning: Mixed fabrics and plastic brims are not standard recycling or compost.

Description: 'A backpack with zippers.' -> This item is miscellaneous.
Reasoning: Mixed textiles, plastic, and metal zippers don’t fit a single category.

Description: 'A rubber band ball (multiple rubber bands).' -> This item is miscellaneous.
Reasoning: Rubber is not typically recycled curbside, nor is it organic or electronic.

Description: 'A vinyl record (music LP).' -> This item is miscellaneous.
Reasoning: Vinyl (PVC) is rarely recycled, not organic, and not electronic.

Description: 'A synthetic wig.' -> This item is miscellaneous.
Reasoning: Composed of synthetic fibers not typically compostable or recyclable.

Description: 'A skateboard deck with grip tape.' -> This item is miscellaneous.
Reasoning: Mixed materials (wood, adhesives, metal) complicate recycling.

Description: 'A trophy with a metal plate on a plastic base.' -> This item is miscellaneous.
Reasoning: Multiple materials are fused, making it hard to separate or recycle.

Description: 'A decorative snow globe with liquid and glitter.' -> This item is miscellaneous.
Reasoning: Glass, water, glitter, and plastic figurines are inseparable.

Description: 'A faux leather wallet.' -> This item is miscellaneous.
Reasoning: Synthetic leather isn’t recyclable or compostable.

Description: 'A wreath made of artificial plastic greenery.' -> This item is miscellaneous.
Reasoning: Plastic greenery is not compostable nor standard recycling.

Description: 'A large vinyl banner from an event.' -> This item is miscellaneous.
Reasoning: Vinyl banners are typically not curbside-recyclable.

Description: 'A car seat (child safety seat).' -> This item is miscellaneous.
Reasoning: Multiple materials, often need specialized disposal programs.

Description: 'A rubber garden hose.' -> This item is miscellaneous.
Reasoning: Hoses are not accepted in recycling facilities and are not organic or electronic.

Description: 'A decorative candle made of multiple layers of wax and dyes.' -> This item is miscellaneous.
Reasoning: Wax and dyes do not fit in recycling or compost.

Description: 'A synthetic foam mattress topper.' -> This item is miscellaneous.
Reasoning: Foam is not readily recyclable or compostable.

Description: 'A bicycle helmet (polystyrene foam + plastic shell).' -> This item is miscellaneous.
Reasoning: Safety helmets are made of layered composites, not standard recyclables.

Description: 'A plush car seat cover.' -> This item is miscellaneous.
Reasoning: Fabric, foam, and sometimes plastics are combined.

Description: 'A broken porcelain vase.' -> This item is miscellaneous.
Reasoning: Ceramics cannot go with regular glass.

Description: 'A rubber dishwashing glove.' -> This item is miscellaneous.
Reasoning: Latex or rubber gloves are not standard recycling or compost.

Description: 'A vinyl shower curtain liner.' -> This item is miscellaneous.
Reasoning: PVC-based materials are not recycled curbside or compostable.

Description: 'A throw rug (polyester blend).' -> This item is miscellaneous.
Reasoning: Textiles with synthetic blends require special textile recycling.

Description: 'A cat scratching post with carpet and cardboard inserts.' -> This item is miscellaneous.
Reasoning: Combination of fabric, cardboard, glue, and wood—difficult to separate.

Description: 'A foam pool noodle.' -> This item is miscellaneous.
Reasoning: Pool noodles are often made from polyethylene foam, not widely recycled.

Description: 'A stuffed animal pet toy (fabric and squeaker).' -> This item is miscellaneous.
Reasoning: Mixed materials with possible plastic squeaker inside.

Description: 'A decorative fish tank ornament (plastic, resin).' -> This item is miscellaneous.
Reasoning: Unlabeled plastic/resin is not standard recycling or compost.

Description: 'A personal keepsake box with metal hinges and velvet lining.' -> This item is miscellaneous.
Reasoning: Multiple materials combined, not suitable for recycling or compost.

Description: 'A foam seat cushion (polyurethane foam).' -> This item is miscellaneous.
Reasoning: Polyurethane foam is not typically recycled or composted.


"""


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
