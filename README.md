
# RecyClean: Real-Time Waste Classification

## 🌱 **Inspiration**
The global waste management crisis inspired us to create RecyClean. Every day, vast amounts of waste end up in the wrong bins due to a lack of awareness and guidance, making recycling inefficient and harming the environment. RecyClean aims to empower users to make eco-friendly waste disposal decisions with the help of AI-driven real-time waste classification.

---

## 🌍 **What it Does**
RecyClean is a real-time waste classification tool that helps users identify waste categories and dispose of waste correctly. With the help of advanced AI technologies, the system:

- **Classifies Waste in Real Time:** Captures live video from a webcam, detects objects using Google Vision, and classifies them into one of five waste categories: Recycling, Organic, Trash, Electronic, or Miscellaneous.
- **Provides Verbal Feedback:** Utilizes Google Text-to-Speech (TTS) to give users an audio response, guiding them on how to dispose of the detected object.

---

## 🛠️ **How We Built It**
RecyClean integrates several technologies to deliver an intuitive and functional solution:

- **Frontend:** OpenCV for capturing and displaying real-time video streams.
- **AI for Object Detection:** Google Vision API detects and labels objects in the video frames.
- **AI for Classification:** OpenAI’s GPT-3.5-turbo model classifies detected objects into appropriate waste categories.
- **Text-to-Speech:** Google Text-to-Speech (gTTS) converts text into speech, providing verbal instructions.
- **Audio Playback:** Uses the system’s native audio player or the `playsound` library to play back TTS-generated audio.

---

## 🔧 **Challenges We Ran Into**

1. **API Integration:** Combining Google Vision and OpenAI APIs required careful coordination to ensure real-time performance.
2. **Real-Time Performance:** Ensuring low latency between detection, classification, and feedback.
3. **Audio Playback:** Cross-platform audio playback had compatibility challenges, which required fallback strategies.
4. **Error Handling:** Managing API errors and temporary file cleanup robustly.

---

## 🏆 **Accomplishments We’re Proud Of**

- **Seamless Integration:** Successfully integrated multiple APIs to create a smooth workflow.
- **Real-Time Feedback:** Achieved minimal delay between object detection and user feedback.
- **Cross-Platform Compatibility:** Designed the system to work on various operating systems.

---

## 🎓 **What We Learned**

1. **AI API Utilization:** Effectively combining the capabilities of different AI APIs (Google Vision and OpenAI GPT-3.5-turbo).
2. **Real-Time Video Processing:** Leveraging OpenCV for efficient video capture and display.
3. **Speech Synthesis:** Using gTTS and system-level audio playback to enhance user interaction.

---

## 🚀 **What’s Next**

1. **Mobile App Development:** Develop a native mobile application to make RecyClean more accessible and portable.
2. **Integration with IoT:** Enhance functionality by integrating with IoT-enabled smart bins for automated waste sorting.
3. **Machine Learning Model:** Replace or complement the Google Vision API with a custom-trained ML model for more specialized waste detection.
4. **Expanded Language Support:** Add multilingual support to reach a broader audience.

---

## ⚙️ **How to Run the Project**

### Prerequisites
1. Install Python (>= 3.8).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up API keys:
   - Google Vision API: Place the service account JSON file as `key.json` in the project directory.
   - OpenAI API: Add your OpenAI API key to `config.json` in the following format:
     ```json
     {
         "OPENAI_API_KEY": "your_openai_api_key_here"
     }
     ```

### Running the Project
1. Run the Python script:
   ```bash
   python recyclean.py
   ```
2. **Controls:**
   - Press **'d'** to detect and classify objects from the video stream.
   - Press **'q'** to quit the application.

---

## 📜 **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 **Contributing**
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

## 🙌 **Acknowledgments**

- **Google Cloud Vision API:** For object detection and labeling.
- **OpenAI:** For GPT-3.5-turbo API.
- **gTTS:** For text-to-speech conversion.
- **OpenCV:** For real-time video capture and display.

Thank you for making a difference with RecyClean!
