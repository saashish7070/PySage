from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

# Load model and tokenizer
model_path = "backend/models/Qwen"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    input_text = request.message
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=200)
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": response_text}
