import json

from openai import OpenAI
from make_prompt import searchVectorDb

client = OpenAI(api_key="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")

def generateResponse(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot designed to help a student."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message


if __name__ == "__main__":
    save_file = r"C:\Users\Gaurav\SIGIR-Chatbot\Task_Theory_Part_1_DB.json"
    with open(save_file, 'r') as f:
        contexts = json.load(f)
    prompt = input("Please enter your question\n")
    new_prompt = searchVectorDb(prompt, contexts)
    output = generateResponse(new_prompt)
    # import ipdb; ipdb.set_trace()