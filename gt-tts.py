from gtts import gTTS
import os
#demo

# Text to be spoken
text = "The quick brown fox jumped over the lazy dog."

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine
tts = gTTS(text=text, lang=language, tld="co.in",slow=False)

# Saving the converted audio to a file
tts.save("output.mp3")

# Playing the converted audio (optional)
os.system("afplay output.mp3")
