import logging
import os

# logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     datefmt='%Y-%m-%d:%H:%M:%S',
#     level=logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("{0}.log".format("app-log"))
fileHandler.setFormatter(logFormatter)

rootLogger.setLevel(logging.INFO)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.INFO)

rootLogger.addHandler(consoleHandler)