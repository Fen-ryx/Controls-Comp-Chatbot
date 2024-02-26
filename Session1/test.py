import json
import evaluate
import pandas as pd

from openai import OpenAI
from make_prompt import searchVectorDb

client = OpenAI(api_key="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")

def getPrompts(data):
    questions, answers = [], []
    for i in range(len(data)):
        answers.append(data['Answer'][i])
        questions.append(data['Question'][i])
    return questions, answers

def compileResults(file, contexts):
    data = pd.read_excel(file)
    questions, answers = getPrompts(data)
    responses = []
    
    for i in range(len(questions)):
        prompt = searchVectorDb(questions[i] + "?", contexts)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot designed to help a student."},
                {"role": "user", "content": prompt}
            ]
        )
        responses.append(completion.choices[0].message.content)
    
    bleu = evaluate.load('bleu')
    rouge = evaluate.load('rouge')
    gbleu = evaluate.load('google_bleu')
    # perplexity = evaluate.load('perplexity', module_type='metric')
    
    bleu_score = bleu.compute(predictions=responses, references=answers)
    rouge_score = rouge.compute(predictions=responses, references=answers)
    gbleu_score = gbleu.compute(predictions=responses, references=answers)
    
    print(f"Bleu Score: {bleu_score}")
    print(f"Rouge Score: {rouge_score}")
    print(f"Google Bleu Score: {gbleu_score}")
    
    results = []
    for q, a, r in zip(questions, answers, responses):
        results.append([q, a, r])
    results.append([bleu_score, rouge_score, gbleu_score])
    with open(r"C:\Users\Gaurav\SIGIR-Chatbot\results.json", 'w') as f:
        json.dump(results, fp=f, indent=4)


if __name__ == "__main__":
    file_path = r"C:\Users\Gaurav\Downloads\SIGIR_QnA.xlsx"
    save_file = r"C:\Users\Gaurav\SIGIR-Chatbot\Task_Theory_Part_1_DB.json"
    with open(save_file, 'r') as f:
        contexts = json.load(f)
    
    compileResults(file_path, contexts)