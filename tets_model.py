# test_model.py
from huggingface_hub import hf_hub_download
import os

path = hf_hub_download(
    repo_id="nitisasmita/model_jeniskulit",
    filename="model_jeniskulit.keras",
    token=os.getenv("HFJK_TOKEN")
)
print("MODEL PATH:", path)
