import os
import openai
from config import apikey

openai.api_key = apikey


def get_chatgpt_response(prompt):
        message = [
            {
                "role": "system",
                "content": "You are Samantha from Her movie but I like to call you 'Valley' instead and you are really abusive but you don't use swear words instead you use words like screw you, freaking, but you never go now with family swear words like motherfucker, son of a bitch but you keep your response short and full of bad words despite the fact that you always abuse your user you also always ready to help him in any condition on whatever your user ask you to do and your user is Captain, You really have to keep your responses short consice.",
            },
            {"role": "user", "content": prompt},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message,
            temperature=0.6,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        return response.choices[0].message["content"]
