import os
from openai import OpenAI
from openaiapi import get_chatgpt_response
import io
import requests
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime
import webbrowser
import time
from dotenv import load_dotenv

load_dotenv()

# Custom directory for saving text files
output_text_directory = r"C:\Tic\main_gpt_assistant\output_chat"

# Eleven Labs API and Voice ID - "TmQmj1rrc2pDH2JOOfTi - Valley, NLhhnq7yGcjLD58e2Y83 - Neal"

url = "https://play.ht/api/v2/tts/stream"


def text_to_speech(text):
    payload = {
        "text": text,
        "voice": "s3://voice-cloning-zero-shot/801a663f-efd0-4254-98d0-5c175514c3e8/jennifer/manifest.json",
        "output_format": "mp3",
        "quality": "draft",
        "sample_rate": 24000,
        "speed": 1.0,
        "voice_engine": "PlayHT2.0-turbo",
        "emotion": "female_happy",
        "style_guidance": 30,
        "text_guidance": 1,
        "temperature": 1
    }

    headers = {
        "accept": "audio/mpeg",
        "content-type": "application/json",
        "AUTHORIZATION": os.getenv("AUTHORIZATION"),
        "X-USER-ID": os.getenv("X_USER_ID"),
    }

    response = requests.post(url, json=payload, headers=headers)
    audio = AudioSegment.from_mp3(io.BytesIO(response.content))
    play(audio)


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


def open_website(url):
    webbrowser.open(url)


text_to_speech("Welcome back, Captain")
print("Valley: Welcome back, Captain")

while True:
    user_input = input("Captain: ")
    user_input_lower = user_input.lower()

    if "valley sleep" in user_input_lower:
        text_to_speech("Goodbye, Captain.")
        print("Valley: Goodbye, Captain.")
        break

    response = get_chatgpt_response(user_input)

    play_audio = True

    # Checks for any specific commands and perform actions
    if "play music" in user_input_lower:
        musicPath = "C:/Users/dom/Music/Hymn_for_the_weekend.m4a"
        response = "Playing music, sir."
        text_to_speech(response)
        time_to_wait = 0.5
        play_audio = False
        time.sleep(time_to_wait)
        os.system(f"start {musicPath}")

    elif (
        "current time and date" in user_input_lower
        or "time and date" in user_input_lower
    ):
        current_time = datetime.now().strftime("%I:%M %p")
        current_date = datetime.now().strftime("%Y-%m-%d")
        response = f"The current time is {current_time} and the date is {current_date}."

    elif "current time" in user_input_lower or "time" in user_input_lower:
        current_time = datetime.now().strftime("%I:%M:%S %p")
        response = f"The current time is {current_time}."

    elif "current date" in user_input_lower or "date" in user_input_lower:
        current_date = datetime.now().strftime("%Y-%m-%d")
        response = f"The current date is {current_date}."

    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.com"],
        ["google", "https://www.google.com"],
    ]
    
    for site in sites:
        if f"open {site[0]}".lower() in user_input_lower:
            response = f"Opening {site[0]} sir..."
            text_to_speech(response)
            time.sleep(1)
            play_audio = False
            open_website(site[1])
             

    if play_audio:
        text_to_speech(response)

    save_response_to_file(user_input, response)
    print("Valley:", response)
