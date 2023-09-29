import os
import openai

openai.api_key = ""


def handle_response(system_role, user_message):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{system_role}."},
            {"role": "user", "content": f"{user_message}"}
        ]
    )
    return completion.choices[0].message
