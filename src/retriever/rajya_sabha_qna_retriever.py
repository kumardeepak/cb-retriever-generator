import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
import uuid
from utils import LOG


class RajyaSabhaQnARetriever():
    def __init__(self, filepath):
        self.filepath   = filepath
        self.device     = "cpu"

        if torch.backends.mps.is_available() == True:
            self.device = "mps"
        else:
            if torch.backends.cuda.is_available() == True:
                self.device = "cuda"
        self.retriever  = SentenceTransformer("flax-sentence-embeddings/all_datasets_v3_mpnet-base", device=self.device)

    def get_records(self):
        df      = pd.read_csv(self.filepath)
        field1s = []
        field2s = []
        field3s = []
        field4s = []
        field5s = []
        field6s = []

        for i, row in df.iterrows():
            field1  = str(uuid.uuid4())
            field1s.append(field1)

            # field2  = [random.random() for _ in range(5)] #self.get_sentence_embedding(row['question_description'])
            field2  = self.get_sentence_embedding(row['question_description'])
            field2s.append(field2)

            field3  = row['answer']
            field3s.append(field3)

            field4  = row['question_description']
            field4s.append(field4)

            field5  = row['question_title']
            field5s.append(field5)

            field6  = row['question_by']
            field6s.append(field6)
        
        return field1s, field2s, field3s, field4s, field5s, field6s

    def get_sentence_embedding(self, text):
        return self.retriever.encode(text)
    
    def format_search_results(self, results, threshold):
        context = []
        for i, result in enumerate(results):
            for j, res in enumerate(result):
                LOG.info("id: [%s], distance: [%f], question: [%s], answer: [%s]", res.id, res.distance, res.entity.get('question'), res.entity.get('answer'))

                if res.distance >= threshold:
                    context.append(' ')
                    context.append(res.entity.get('answer'))

        return ' '.join(context)
