from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import pytesseract
from PIL import Image
import PyPDF2

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Conversion route
@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    voice = request.form.get('voice', 'male')  # male/female
    speed = request.form.get('speed', 'normal')  # slow/normal/fast

    text = ""
    filename = file.filename

    # PDF
    if filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    # Image
    elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img = Image.open(file)
        text = pytesseract.image_to_string(img)

    else:
        return "Invalid file format. Only PDF and Image allowed."

    # Adjust speed for gTTS
    tts_speed = True if speed == 'fast' else False
    tts = gTTS(text=text, lang='en', slow=(speed=='slow'))

    # Save audio file
    audio_path = "output.mp3"
    tts.save(audio_path)

    return render_template('result.html', audio_file=audio_path, text=text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
