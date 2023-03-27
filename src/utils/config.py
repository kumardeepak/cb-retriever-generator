import os
import time
import json

DEBUG                   = False
API_URL_PREFIX          = "/"
HOST                    = '0.0.0.0'
PORT                    = os.environ.get('PORT', 5001)
DATA_DIR                = os.environ.get('DATA_DIR', '/Users/kumar_cont23/Downloads/')

ENABLE_CORS             = False

VECTOR_DB_HOST              = os.environ.get('VECTOR_DB_HOST', "localhost")
VECTOR_DB_PORT              = os.environ.get('VECTOR_DB_PORT', 19530)
VECTOR_DB_ALIAS             = os.environ.get('VECTOR_DB_ALIAS', "default")

RAJYA_SABHA_FILEPATH_1      = os.environ.get('RAJYA_SABHA_FILEPATH_1', '/Users/kumar.deepak/Downloads/temp/rajyasabha/rajya_sabha_faqs_v1.csv')
