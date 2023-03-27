from models import RajyaSabhaQnAModel
from retriever import RajyaSabhaQnARetriever
from generator import ConditionalGenerator
from transport import VectorDB
import utils.config as CONFIG
from utils import LOG

def main():
    dbConn          = VectorDB(CONFIG.VECTOR_DB_HOST, CONFIG.VECTOR_DB_PORT, CONFIG.VECTOR_DB_ALIAS)
    dbConn.connect()

    qnaCollection   = RajyaSabhaQnAModel("QNA_RAJYA_FAQ_v1", 768)
    qnaRetriever    = RajyaSabhaQnARetriever(CONFIG.RAJYA_SABHA_FILEPATH_1)
    generator       = ConditionalGenerator()

    field1s, field2s, field3s, field4s, field5s, field6s = qnaRetriever.get_records()
    insert_count    = qnaCollection.insert(field1s, field2s, field3s, field4s, field5s, field6s)
    LOG.info("inserted %d records", insert_count)

    search_text     = 'How many members does each state have in Rajya Sabha?'
    search_vector   = qnaRetriever.get_sentence_embedding(search_text)
    results         = qnaCollection.search(search_vector, 1)
    context         = qnaRetriever.format_search_results(results, 0.30)

    answer          = generator.generate_answer(search_text, context)

    # for i, result in enumerate(results):
    #     for j, res in enumerate(result):
    #         LOG.info("id: [%s], distance: [%f], question: [%s], answer: [%s]", res.id, res.distance, res.entity.get('question'), res.entity.get('answer'))

    LOG.info("answer: %s", answer)

    # qnaCollection.drop()
    dbConn.disconnect()

def get_user_input(collection, retriever, generator):

    while True:
        val             = input("Enter your question: << ")
        if val == 'quit' or val == 'exit':
            return
        else:
            if len(val) < 4:
                LOG.info("question too short to answer")
            else:
                search_text     = val
                search_vector   = retriever.get_sentence_embedding(search_text)
                results         = collection.search(search_vector, 1)
                context         = retriever.format_search_results(results, 0.000)

                answer          = generator.generate_answer(search_text, context)
                LOG.info("Answer: >>> %s\n", answer)

if __name__ == '__main__':
    LOG.info("starting application")
    dbConn          = VectorDB(CONFIG.VECTOR_DB_HOST, CONFIG.VECTOR_DB_PORT, CONFIG.VECTOR_DB_ALIAS)
    dbConn.connect()

    qnaCollection   = RajyaSabhaQnAModel("QNA_RAJYA_FAQ_v1", 768)
    qnaRetriever    = RajyaSabhaQnARetriever(CONFIG.RAJYA_SABHA_FILEPATH_1)
    generator       = ConditionalGenerator()

    get_user_input(qnaCollection, qnaRetriever, generator)

    dbConn.disconnect()

    # main()
