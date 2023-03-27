from pymilvus import connections
from utils import LOG

class VectorDB():
    def __init__(self, hostname, port, alias):
        self.hostname   = hostname
        self.port       = port
        self.alias      = alias

    def connect(self):
        try:
            LOG.info("Trying to connect to %s:%d", self.hostname, self.port)
            connections.connect(host=self.hostname, port=self.port, alias=self.alias)
        except Exception as e:
            LOG.error("connection to %s, failed", self.hostname)
            LOG.error(e)

    def disconnect(self):
        LOG.info("Disconnecting ")
        connections.disconnect(self.alias)

    