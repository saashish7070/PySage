from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# Download and save the model locally
def download_and_save_model(model_name, local_dir):
    if not os.path.exists(local_dir):
        print(f"Downloading and saving {model_name} to {local_dir}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(local_dir)

        model = AutoModelForCausalLM.from_pretrained(model_name)
        model.save_pretrained(local_dir)
        print("Download complete.")
    else:
        print(f"Model already downloaded in {local_dir}")

# Model details
model_name = "codeparrot/codeparrot-small"
local_dir = "./models/codeparrot-model-text"

# Download the model if not already present
download_and_save_model(model_name, local_dir)

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(local_dir)
model = AutoModelForCausalLM.from_pretrained(local_dir)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSocket

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        if not data or "input" not in data:
            return jsonify({"error": "Invalid input. 'input' field is required."}), 400

        input_text = data["input"]
        max_length = data.get("max_length", 50)
        temperature = max(0.1, min(data.get("temperature", 1.0), 2.0))
        top_k = data.get("top_k", 50)
        top_p = data.get("top_p", 0.95)

        inputs = tokenizer(
            input_text,
            max_length=512,
            truncation=True,
            return_tensors="pt"
        )

        outputs = model.generate(
            inputs.input_ids,
            max_length=max_length,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@socketio.on('message')
def handle_message(data):
    try:
        input_text = data.get("input", "")
        max_length = data.get("max_length", 50)
        temperature = max(0.1, min(data.get("temperature", 1.0), 2.0))
        top_k = data.get("top_k", 50)
        top_p = data.get("top_p", 0.95)

        inputs = tokenizer(
            input_text,
            max_length=512,
            truncation=True,
            return_tensors="pt"
        )

        outputs = model.generate(
            inputs.input_ids,
            max_length=max_length,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        emit('response', {"response": response})
    except Exception as e:
        emit('error', {"error": str(e)})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
