from transformers import BartTokenizer, BartForConditionalGeneration
from utils import LOG

class ConditionalGenerator():
    def __init__(self):
        self.tokenizer  = BartTokenizer.from_pretrained('vblagoje/bart_lfqa')
        self.generator  = BartForConditionalGeneration.from_pretrained('vblagoje/bart_lfqa').to()

    def generate_answer(self, question, context):
        query = f"question: {question} context: {context}"

        LOG.info("context for generation: %s", query)

        # tokenize the query to get input_ids
        inputs = self.tokenizer([query], max_length=1024, return_tensors="pt")
        # use generator to predict output ids
        ids = self.generator.generate(inputs["input_ids"], num_beams=2, min_length=20, max_length=100)
        # use tokenizer to decode the output ids
        answer = self.tokenizer.batch_decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        return answer
