from flask import Flask, render_template, request, send_from_directory, jsonify, url_for
from gtts import gTTS
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Temporary directory for saving audio files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'audio')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Supported language codes with labels and tlds
VOICE_OPTIONS = {
    "en": {"name": "English (US)", "tld": "com"},
    "en-uk": {"name": "English (UK)", "tld": "co.uk"},
    "en-au": {"name": "English (Australia)", "tld": "com.au"},
    "es": {"name": "Spanish", "tld": "es"},
    "fr": {"name": "French", "tld": "fr"},
    "de": {"name": "German", "tld": "de"},
    "it": {"name": "Italian", "tld": "it"},
    "ja": {"name": "Japanese", "tld": "co.jp"},
    "ko": {"name": "Korean", "tld": "co.kr"},
    "pt-br": {"name": "Portuguese (Brazil)", "tld": "com.br"},
    "ru": {"name": "Russian", "tld": "ru"},
    "zh-cn": {"name": "Chinese (Simplified)", "tld": "com.cn"},
}

@app.route('/')
def index():
    return render_template('index.html', voices=VOICE_OPTIONS)

@app.route('/convert', methods=['POST'])
def convert_to_speech():
    data = request.json
    text = data.get('text')
    lang = data.get('lang')

    if not text or not lang or lang not in VOICE_OPTIONS:
        return jsonify({"error": "Text and valid language are required"}), 400

    tld = VOICE_OPTIONS[lang]['tld']
    filename = f"{next(tempfile._get_candidate_names())}.mp3"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        tts = gTTS(text=text, lang=lang.split('-')[0], tld=tld)
        tts.save(file_path)
        audio_url = url_for('serve_audio', filename=filename)
        return jsonify({"audio_url": audio_url})
    except Exception as e:
        logging.exception("Error in conversion:")
        return jsonify({"error": str(e)}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
