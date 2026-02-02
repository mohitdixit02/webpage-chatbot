import os
from config import logger
class EnvironmentProvider:
    def __init__(self):
        logger.info("Loading environment settings...")
        self.TOP_K_DOCS_IN_DB = int(os.getenv("TOP_K_DOCS_IN_DB", 5))
        self.TOP_K_DOCS_IN_RETRIEVER = int(os.getenv("TOP_K_DOCS_IN_RETRIEVER", 2))
        
        self.ACCEPTABLE_RELEVANCE_SCORE_DB = float(os.getenv("ACCEPTABLE_RELEVANCE_SCORE_DB", 0.4))
        self.RELEVANCE_SCORE_THRESHOLD_DB = float(os.getenv("RELEVANCE_SCORE_THRESHOLD_DB", 0.6))
        
        self.ACCEPTABLE_RELEVANCE_SCORE_RETRIEVER = float(os.getenv("ACCEPTABLE_RELEVANCE_SCORE_RETRIEVER", 0.4))
        self.RELEVANCE_SCORE_THRESHOLD_RETRIEVER = float(os.getenv("RELEVANCE_SCORE_THRESHOLD_RETRIEVER", 0.75))
        
        self.AUTO_COMPRESS = bool(int(os.getenv("AUTO_COMPRESS", "True") == "True"))
        self.MAX_ALLOWED_SOURCES_IN_DB = int(os.getenv("MAX_ALLOWED_SOURCES_IN_DB", 10))
        
        self.LOCAL_EMBEDDING_MODEL = bool(int(os.getenv("LOCAL_EMBEDDING_MODEL", "False") == "True"))
        self.HF_TOKEN = os.getenv("HF_TOKEN", "")