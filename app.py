from flask import Flask, request, render_template, url_for
from flask_cors import CORS
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')

@app.route('/', methods=['POST'])
def text_to_speech():
    try:
        # Get form data
        text = request.form.get('text', '').strip()
        language = request.form.get('language', 'en').strip()

        # Validate input
        if not text:
            return render_template('index.html', error="No text provided")

        # Generate a unique filename for the audio file
        unique_filename = f"audio/{uuid.uuid4()}.mp3"
        file_path = os.path.join('static', unique_filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Generate the audio file using gTTS
        tts = gTTS(text=text, lang=language)
        tts.save(file_path)

        # Debugging: Print the file path and URL
        print(f"Generated audio file path: {file_path}")
        print(f"Audio file URL: {url_for('static', filename=unique_filename)}")

        # Pass the audio file to the template for playback
        return render_template('index.html', audio_file=unique_filename)

    except Exception as e:
        # Handle errors and display them on the page
        return render_template('index.html', error=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0')