# Sentiment Analysis API

This project provides a Flask-based sentiment analysis API that allows users to analyze the sentiment of text using either a custom fine-tuned model or the Llama 3 model via the Groq Cloud API.

## Installation

### Prerequisites
- Python 3.8 or later
- pip
- A Hugging Face account (for accessing the fine-tuned model)
- A Groq Cloud API key (for accessing Llama 3)

### Install Dependencies

```sh
pip install -r requirements.txt
```

## Running the Notebook

To test the model in a Jupyter notebook, run:

```sh
jupyter notebook
```

Open the provided notebook and execute the cells to test the fine-tuned model.

## Running the API Locally

1. Set up environment variables:
   ```sh
   export GROQ_API_KEY="your_api_key_here"
   ```
   (On Windows, use `set GROQ_API_KEY=your_api_key_here`)

2. Start the Flask server:
   ```sh
   python app.py
   ```
   The server will run on `http://127.0.0.1:5000/`

## Using the Endpoints

### 1. Analyze Sentiment

#### Request

**POST** `/analyze/`

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Body:**
```json
{
  "text": "This is a great product!",
  "model": "custom"  
}
```
- `model` can be either `custom` (fine-tuned model) or `llama` (Groq Llama 3 model).

#### Response
```json
{
  "sentiment": "positive",
  "confidence": 0.95
}
```

### Testing via Curl
```sh
curl -X POST http://127.0.0.1:5000/analyze/ \  
     -H "Content-Type: application/json" \  
     -d '{"text": "I love this!", "model": "llama"}'
```

### Testing via Python Requests

```python
import requests

url = "http://127.0.0.1:5000/analyze/"
data = {"text": "I love this!", "model": "llama"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### Testing via postman 
[postman webversion](https://web.postman.co/workspace/My-Workspace~033722f5-7df0-48d8-8e76-3c5771a8bbe3/overview)

## Notes
- Ensure that the Hugging Face model is correctly uploaded and accessible.
- The Groq API key must be valid to access Llama 3.

## License
This project is for educational purposes only.

