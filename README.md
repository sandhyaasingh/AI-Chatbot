# AI Chatbot using Deep Learning and NLP  
This project implements an AI chatbot using Python, NLTK, and a Feedforward Neural Network. It includes intent recognition, API integrations, and a front-end interface.

## Features  
- Intent recognition using NLP.  
- Feedforward Neural Network for predicting user intents.  
- Integrated with a chatbot API for responses.  
- Flask API for chatbot interaction.  
- Web UI built with HTML, CSS, JavaScript, and ReactJS.  

## Setup  

```bash
# Create a virtual environment  
python -m venv venv  
venv\Scripts\activate  

# Install dependencies  
pip install -r requirements.txt  
```

## Download NLTK Data  

```python
import nltk
nltk.download('punkt')
```

## Model Training  

```bash
python train.py  
```

## Running the Chatbot  

```bash
python chat.py  
```

## API Integration  

```python
import requests

def chatbot_response(user_input):
    api_url = "https://api.example.com/chat"
    payload = {"message": user_input}
    response = requests.post(api_url, json=payload)
    return response.json().get("answer", "I couldn't understand that.")
```

## API Deployment  

```python
from flask import Flask, request, jsonify
from chat import get_response

app = Flask(__name__)

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    return jsonify({"answer": response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
```

## Running API Locally  

```bash
python app.py  
```

## Web UI  
Includes a chatbot interface built using HTML, CSS, and JavaScript (ReactJS), customizable as needed.  
