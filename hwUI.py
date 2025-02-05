from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import groq

app = Flask(__name__)

# 加载自定义模型
custom_model = AutoModelForSequenceClassification.from_pretrained("fujiazhiyu/my-finetuned-distilbert-spam-classifier")
custom_tokenizer = AutoTokenizer.from_pretrained("fujiazhiyu/my-finetuned-distilbert-spam-classifier")

# Initialize Groq API client
groq_client = groq.Client(api_key="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")

def get_sentiment(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=-1)
    sentiment = "positive" if probs[0][1] > 0.5 else "negative"
    confidence = probs[0][1].item() if sentiment == "positive" else probs[0][0].item()
    return sentiment, confidence

def analyze_with_llama(text):
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",  # or "llama3-70b-8192"
        messages=[
            {"role": "system", "content": "Analyze the sentiment of the given text. Respond with either 'positive', 'negative', or 'neutral'."},
            {"role": "user", "content": text}
        ],
        temperature=0.3,  
        max_tokens=20  
    )

    llama_response = response.choices[0].message.content.strip().lower()

    # judge sentiment
    if "positive" in llama_response:
        sentiment = "positive"
    elif "negative" in llama_response:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    confidence = 0.85  # mock
    return sentiment, confidence

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        model_type = request.form['model']
        
        if model_type == 'custom':
            sentiment, confidence = get_sentiment(text, custom_model, custom_tokenizer)
        elif model_type == 'llama':
            sentiment, confidence = analyze_with_llama(text)
        else:
            return render_template('index.html', error="Invalid model type")
        
        return render_template('index.html', text=text, model=model_type, sentiment=sentiment, confidence=confidence)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
