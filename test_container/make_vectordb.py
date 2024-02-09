import os
import json
import pandas as pd
from sentence_transformers import SentenceTransformer

LIMIT = 384


class Make_Retrieval_Database():
    def __init__(self, contexts, save_file, code_filepath):
        self.contexts = contexts
        self.save_file = save_file
        self.code_info = pd.read_excel(code_filepath, sheet_name='Module1_Code_QnA')
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def createDatabase(self):
        chunks = self.chunker()
        # import ipdb; ipdb.set_trace()
        embeddings = self.makeDenseEmbeddings(chunks)
        
        i, self.database = 0, list()
        for chunk, embedding in zip(chunks, embeddings):
            self.database.append({"id": i, "context": chunk, "embedding": embedding.tolist()})
            i += 1
        
        col1, col2, _, _ = self.code_info.columns
        for topic, desc in zip(self.code_info[col1], self.code_info[col2]):
            info = topic + "\n" + desc
            embedding = self.makeDenseEmbeddings([info])
            self.database.append({"id": i, "context": info, "embedding": embedding.tolist()})
            i += 1
        
        with open(self.save_file, 'w') as f:
            json.dump(self.database, fp=f, indent=4)
    
    def chunker(self):
        chunks = []
        all_contexts = self.contexts.split('.')
        chunk = []
        for context in all_contexts:
            chunk.append(context)
            if len(chunk) >= 3 and len('.'.join(chunk)) > LIMIT:
                chunks.append('.'.join(chunk).strip()+'.')
                chunk = chunk[-2:]
        if chunk is not None:
            chunks.append('.'.join(chunk))
        return chunks
    
    def makeDenseEmbeddings(self, chunks):
        embeddings = self.model.encode(chunks)
        return embeddings


if __name__ == "__main__":
    code_filepath = os.path.join(os.getcwd(), "Code_QnA.xlsx")
    filepath = os.path.join(os.getcwd(), "Task_Theory_Part_1.txt")
    save_file = os.path.join(os.getcwd(), "Task_Theory_Part_1_DB.json")
    
    with open(filepath, 'r', encoding="utf8") as f:
        contexts = f.read()
    
    retrievedb = Make_Retrieval_Database(contexts, save_file, code_filepath)
    retrievedb.createDatabase()