import pyttsx3
import wave
from pydub import AudioSegment
import os

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Set properties (Optional)
engine.setProperty('rate', 180)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Text to be spoken
text = 'The quick brown fox jumped over the lazy dog.'

engine.say(text)

# Wait for the speech to be saved
engine.runAndWait()