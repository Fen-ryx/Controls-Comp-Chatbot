import os
import json
import evaluate
import pandas as pd

from openai import OpenAI
from make_prompt import searchVectorDb

EXIT_CODE = 8465
client = OpenAI(api_key="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")


def interactions(contexts, instructions):
    past, i = "", 0
    
    while (True):
        i += 1
        clean_prompt = input(f"Enter your question. To end this thread, please enter the exit code: {EXIT_CODE}\n")
        if (clean_prompt.isnumeric() and (int)(clean_prompt) == EXIT_CODE):
            break
        prompt = past + "\n" + searchVectorDb(clean_prompt, contexts)
        prompt = prompt + instructions
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot designed to help a novice in the domain of Control Theory pertaining to Robotics."},
                {"role": "user", "content": prompt}
            ]
        )
        response = completion.choices[0].message.content
        print(response)
        past = past + clean_prompt + response
        
        if (i % 5 == 0):
            past = past + "Please summarize the above interaction in brief. Ensure your responses are not long."
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a chatbot designed to help a novice in the domain of Control Theory pertaining to Robotics. You are meant to summarize a series of question-answer pairs in brief."},
                    {"role": "user", "content": past}
                ]
            )
            past = completion.choices[0].message.content


if __name__ == "__main__":
    save_file = os.path.join(os.getcwd(), "Task_Theory_Part_1_DB.json")
    with open(save_file, 'r') as f:
        contexts = json.load(f)
    
    instruction = "Please include at least one relevant example in your response. Additionally, please structure your response in the following format: a) Theory \nb)Mathematical Example. Also, please try and keep your responses short."# \n c) Code (if applicable)"
    interactions(contexts, instruction)