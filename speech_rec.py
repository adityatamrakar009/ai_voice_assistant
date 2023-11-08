import os
import openai
from openaiapi import get_chatgpt_response
from elevenlabsapi import ttsapikey
import io
import requests
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime
import speech_recognition as sr

# Custom directory for saving text files
output_text_directory = "C:/Tic/gpt_assistant/output_chat"  # Text directory

# Eleven Labs API and Voice ID - "TmQmj1rrc2pDH2JOOfTi"
ELEVEN_LABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/TmQmj1rrc2pDH2JOOfTi"
ELEVEN_LABS_API_KEY = ttsapikey

def text_to_speech(text):
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY,
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(ELEVEN_LABS_API_URL, json=data, headers=headers)

    audio = AudioSegment.from_mp3(io.BytesIO(response.content))
    play(audio)  # Play the audio

def save_response_to_file(prompt, response):
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y-%m-%d")

    with open(
        os.path.join(output_text_directory, "output.txt"),
        "a",
        encoding="utf-8",
    ) as text_file:
        text_file.write(
            f"Prompt ({current_time}) ({current_date}) - {prompt}\nResponse - {response}\n\n"
        )

recognizer = sr.Recognizer()
phrase_time_limit = 3  # Maximum time (in seconds) for user to complete a phrase

def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Alfred: Say 'bus' to start the conversation.")
        audio = recognizer.listen(source, phrase_time_limit=phrase_time_limit)

    try:
        wake_word = recognizer.recognize_google(audio, language="en-in")
        if "bus" in wake_word:
            print("Alfred: Conversation started. Speak now.")
            while True:
                user_input = input("Master Wayne: ")
                response = get_chatgpt_response(user_input)
                text_to_speech(response)  # ChatGPT Response as audio
                save_response_to_file(user_input, response)  # Saving ChatGPT response and the prompt in a single text file
                print("Alfred:", response)
    except sr.UnknownValueError:
        print("Alfred: I didn't hear the wake word. Please try again.")

while True:
    listen_for_wake_word()
