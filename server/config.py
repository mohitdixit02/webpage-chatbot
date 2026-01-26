print("Loading configuration...")
import os
cache_dir = 'D:/Development/ML/Deep Learning/GenAI/.hf_cache'
os.environ['HF_HOME'] = cache_dir
os.environ['TRANSFORMERS_CACHE'] = cache_dir
os.environ['HF_DATASETS_CACHE'] = cache_dir
os.environ["SENTENCE_TRANSFORMERS_HOME"] = cache_dir
os.makedirs(cache_dir, exist_ok=True)

# HF login
from huggingface_hub import login
from dotenv import load_dotenv
load_dotenv()
login(os.getenv("HF_TOKEN"))

import transformers
print(transformers.file_utils.default_cache_path)
print(f"Using cache directory: {cache_dir}")
print("Configuration loaded successfully.")
    