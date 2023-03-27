from pymilvus import (
    connections,
    FieldSchema, CollectionSchema, DataType,
    Collection,
    utility
)
from utils import LOG

class RajyaSabhaQnAModel ():
    def __init__(self, name, vector_dim):
        self.schema_name                    = name
        self.record_id                      = 'record_id'
        self.vector_dim                     = vector_dim
        self.vector_name                    = 'question_embedding'

        self.metadata_answer_name           = 'answer'
        self.metadata_answer_max_length     = 65000

        self.metadata_question_name          = 'question'
        self.metadata_question_max_length    = 65000
        
        self.metadata_title_name            = 'question_title'
        self.metadata_title_max_length      = 200

        self.metadata_asked_by_name         = 'asked_by'
        self.metadata_asked_by_max_length   = 200

        self.collection                     = None

        self.nprobe                         = 16
        self.index_type                     = 'IVF_FLAT'
        self.metric_type                    = 'L2'
        self.nlist                          = 1024

        if self.is_created() == False:
            LOG.info("collection doesn't exist, creating now")
            self.create()
            self.create_index()
            self.collection.load()
        else:
            LOG.info("collection exists, loading now")
            self.load()

    def create(self):
        field1  = FieldSchema(name=self.record_id, dtype=DataType.VARCHAR, max_length=37, description="uuid4", is_primary=True)
        field2  = FieldSchema(name=self.vector_name, dtype=DataType.FLOAT_VECTOR, description="float vector", dim=self.vector_dim, is_primary=False)
        field3  = FieldSchema(name=self.metadata_answer_name, dtype=DataType.VARCHAR, max_length=self.metadata_answer_max_length, description="answer", is_primary=False)
        field4  = FieldSchema(name=self.metadata_question_name, dtype=DataType.VARCHAR, max_length=self.metadata_question_max_length, description="question", is_primary=False)
        field5  = FieldSchema(name=self.metadata_title_name, dtype=DataType.VARCHAR, max_length=self.metadata_title_max_length, description="title", is_primary=False)
        field6  = FieldSchema(name=self.metadata_asked_by_name, dtype=DataType.VARCHAR, max_length=self.metadata_asked_by_max_length, description="asked by", is_primary=False)

        schema  = CollectionSchema(fields=[field1, field2, field3, field4, field5, field6], description="question answer collection")
        
        try:
            self.collection = Collection(name=self.schema_name, data=None, schema=schema, properties={"collection.ttl.seconds": 1800})
            LOG.info("collection %s, creation successful", self.schema_name)
        except Exception as e:
            LOG.error("collection %s, creation failed", self.schema_name)
            LOG.error(e)

    def drop(self):
        LOG.info("dropping collection %s", self.schema_name)
        self.collection.drop()

    def load(self):
        self.collection = Collection(self.schema_name)
        self.collection.load()

    def release(self):
        self.collection.release()
    
    def total_count(self):
        return self.collection.num_entities
    
    def create_index(self):
        index_param = {
            "index_type": self.index_type,
            "params": {
                "nlist": self.nlist
            },
            "metric_type": self.metric_type
        }

        try:
            self.collection.create_index(self.vector_name, index_param)
        except Exception as e:
            LOG.error("unable to create index for %s", self.vector_name)
            LOG.error(e)

    def drop_index(self):
        self.collection.drop_index()
    
    def insert(self, field1s, field2s, field3s, field4s, field5s, field6s):
        data = [
            field1s, field2s, field3s, field4s, field5s, field6s
        ]
    
        try:
            self.collection.insert(data)
            self.flush()
            LOG.info("inserted record successfully")
        except Exception as e:
            LOG.error("unable to insert entries for %s", self.schema_name)
            LOG.error(e)
            return 0
    
        return self.total_count()
    
    def flush(self):
        self.collection.flush()

    def is_created(self):
        return utility.has_collection(self.schema_name)

    def search(self, search_vector, limit):
        search_param = {
            "data": [search_vector],
            "anns_field": self.vector_name,
            "param": {
                "metric_type": self.metric_type,
                "params": {
                            "nprobe": self.nprobe
                        }
            },
            "limit": limit,
            "output_fields": [self.metadata_question_name, self.metadata_answer_name]
            }
        results = self.collection.search(**search_param)
        return results
