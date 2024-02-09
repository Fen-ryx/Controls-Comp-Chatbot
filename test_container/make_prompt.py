import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

TOP_K = 3
model = SentenceTransformer('all-MiniLM-L6-v2')

def searchVectorDb(prompt, contexts):
    encoding = model.encode(prompt)
    scores = []
    for context in contexts:
        i, _, emb = context['id'], context['context'], np.array(context['embedding'])
        cos_score = computeCosineSimilarity(encoding, emb)
        scores.append([i, cos_score])
    
    appends = ""
    scores.sort(key = lambda x: x[1], reverse=True)
    for i in range(TOP_K):
        idx, _ = scores[i]
        appends += contexts[idx]['context']
        # import ipdb; ipdb.set_trace()
    return appends + '\n' + prompt

def computeCosineSimilarity(prompt, vec):
    return np.dot(prompt, np.squeeze(vec)) / (np.sqrt(np.sum(prompt**2)) * np.sqrt(np.sum(vec**2)))


if __name__ == "__main__":
    save_file = os.path.join(os.getcwd(), "Task_Theory_Part_1_DB.json")
    with open(save_file, 'r') as f:
        contexts = json.load(f)
    prompt = input()
    
    new_prompt = searchVectorDb(prompt, contexts)
    print(new_prompt)