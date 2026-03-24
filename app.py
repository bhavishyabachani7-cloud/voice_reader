from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import pytesseract
from PIL import Image
import PyPDF2

app = Flask(__name__)

# Fix Tesseract path for Render
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading page: {e}"

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    voice = request.form.get('voice', 'male')  # male/female
    speed = request.form.get('speed', 'normal')  # slow/normal/fast

    text = ""
    filename = file.filename
    temp_path = "/tmp/" + filename
    file.save(temp_path)

    # PDF
    if filename.lower().endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(temp_path)
        for page in pdf_reader.pages:
            text += page.extract_text()

    # Image
    elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img = Image.open(temp_path)
        text = pytesseract.image_to_string(img)

    else:
        return "Invalid file format. Only PDF and Image allowed."

    # gTTS audio save
    tts_speed = (speed == 'slow')
    tts = gTTS(text=text, lang='en', slow=tts_speed)
    audio_path = "/tmp/output.mp3"
    tts.save(audio_path)

    return render_template('result.html', audio_file=audio_path, text=text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
