import logging
logging.basicConfig(
    level=logging.INFO,  # or DEBUG, WARNING, etc.
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Logger configured successfully.")
logger.info("Starting configuration setup...")

# Load environment variables
logger.info("Loading environment variables...")
import os
from dotenv import load_dotenv
load_dotenv()

# Cache Directories Setup
isLocalEmbeddingModel = os.getenv("LOCAL_EMBEDDING_MODEL", "False") == "True"
if isLocalEmbeddingModel:
    logger.info("Local embedding model is enabled.")
    logger.info("Setting up cache directories...")
    cache_dir = os.getenv("HF_CACHE_DIR", "./hf_cache")
    os.environ['HF_HOME'] = cache_dir
    os.environ['TRANSFORMERS_CACHE'] = cache_dir
    os.environ['HF_DATASETS_CACHE'] = cache_dir
    os.environ["SENTENCE_TRANSFORMERS_HOME"] = cache_dir
    os.makedirs(cache_dir, exist_ok=True)

    # HF login - only required for some models
    logger.info("Logging into Hugging Face...")
    from huggingface_hub import login
    login(os.getenv("HF_TOKEN"))
    
    import transformers
    logger.info("Default cache directory: %s", transformers.file_utils.default_cache_path)
    logger.info("Custom cache directory set to: %s", cache_dir)
    logger.info("Configuration setup completed.")
else:
    logger.info("Local embedding model is disabled. Using default cache settings.")
