# Handles environment + Hugging Face client.
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load .env
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env file")

# Initialize client
client = InferenceClient(
    model="meta-llama/Llama-3.1-8B-Instruct",
    token=HF_TOKEN
)
