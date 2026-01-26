import logging
logging.basicConfig(
    level=logging.INFO,  # or DEBUG, WARNING, etc.
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger.info("Logger configured successfully.")
logger.info("Starting configuration setup...")
import os
cache_dir = 'D:/Development/ML/Deep Learning/GenAI/.hf_cache'
os.environ['HF_HOME'] = cache_dir
os.environ['TRANSFORMERS_CACHE'] = cache_dir
os.environ['HF_DATASETS_CACHE'] = cache_dir
os.environ["SENTENCE_TRANSFORMERS_HOME"] = cache_dir
os.makedirs(cache_dir, exist_ok=True)

# HF login
logger.info("Logging into Hugging Face...")
from huggingface_hub import login
from dotenv import load_dotenv
load_dotenv()
login(os.getenv("HF_TOKEN"))

import transformers
logger.info("Default cache directory: %s", transformers.file_utils.default_cache_path)
logger.info("Custom cache directory set to: %s", cache_dir)
logger.info("Configuration setup completed.")
    