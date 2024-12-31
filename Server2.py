from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Specify the local directory to save the model
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

# Define model details
model_name = "codeparrot/codeparrot-small"
local_dir = "./codeparrot-model"

# Download and save the model locally
download_and_save_model(model_name, local_dir)

# Load the model and tokenizer from local storage
tokenizer = AutoTokenizer.from_pretrained(local_dir)
model = AutoModelForCausalLM.from_pretrained(local_dir)

# Set up the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Parse request data
        data = request.json
        if not data or "input" not in data:
            return jsonify({"error": "Invalid input. 'input' field is required."}), 400

        input_text = data["input"]
        max_length = data.get("max_length", 50)
        temperature = data.get("temperature", 1.0)
        top_k = data.get("top_k", 50)
        top_p = data.get("top_p", 0.95)

        # Tokenize input
        inputs = tokenizer(input_text, return_tensors="pt")

        # Generate output with sampling parameters
        outputs = model.generate(
            inputs.input_ids,
            max_length=max_length,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            do_sample=True
        )

        # Decode output
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
