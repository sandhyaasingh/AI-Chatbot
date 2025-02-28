# AI Chatbot using Deep Learning and Natural Language Processing
* Test out my chatbot at my personal portfolio: https://ongaunjie.com
* **IMPORTANT NOTE:** If the chatbot is not responding, it is because it takes about 2-5 minutes for it to spin up. This is due to the limitations of free deployments on [Render](https://render.com/). The service will go into hibernation mode after 15 minutes of inactivity.

# To learn more about how it works and how to train a custom chatbot, please read below:
## Overview
### This repository covers four main components:
* Development of an intent-based chatbot using NLTK and Deep Learning models. 
* Integrating the Chatbot with APIs (Weather API, Movie API) and also parsing data from wikipedia using the wikipedia library in python.
* Establishment of an API endpoint using the flask framework.
* Creation of a user interface for the chatbot using JavaScript, HTML, CSS, and ReactJS, ensuring a seamless and interactive user experience.

## a) Creating the chatbot using NLTK and Feedforward Neural Network (FNN):

## Chatbot Features
- **Intent Recognition:** Utilizes Natural Language Processing to recognize user intents.
- **NLTK Library:** Leverages the NLTK library for NLP tasks such as tokenization, stemming and Bag of Words.
- **Deep Learning Model:** Implements a Feedforward Neutral-Network for predicting user intents. 

## Chatbot applications
* Customer Support: Implementing chatbots for various industries, such as e-commerce, healthcare, finance, and technology, providing efficient and responsive customer support services.

# General process of creating a functional intent-based chatbot:
## 1) Data Preparation: 
* Preparing a dataset that includes examples of user inputs and corresponding intents. Each input is associated with a specific intent.

### A snippet of the data used for training, **the data are in the form of .json format**
```
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": [
        "Hi",
        "Hey",
        "How are you",
        "Hello",
        "Good day",
        "Yo"
      ],
      "responses": [
        "Hey :-)",
        "Hello, thanks for visiting",
        "Hi there, what can I do for you?",
        "Hi there, how can I help?",
        "Greetings!",
        "Good to see you!",
        "Hello, how can I assist you today?",
        "Hi! I'm here to help.",
        "Welcome! How can I be of service?",
        "Hello, what can I answer for you?"
    ]
    },
```

## 2) Data preprocessing: 
### Before model training, it is necessary to perform tokenization, stemming, and create a Bag of Words representation for the intents.
* Tokenization is used to break down user inputs and intents into individual words.
* Stemming is applied to reduce words to their base form, helping the model handle variations.
* Bag of Words is a representation of the intents, creating a numerical format for training the machine learning model.

## 3) Model Training: 
* The prepared dataset, including tokenized and preprocessed intents, is used to train a Feedforward Neural Network (FNN).
* The FNN is implemented using a deep learning framework, such as PyTorch or TensorFlow. (For this repo, I am using PyTorch)
* The neural network architecture comprises input, hidden, and output layers, with appropriate activation functions like ReLU for non-linearity.
* During training, the model learns to map tokenized input sequences to corresponding intents.
* The loss function is employed to measure the difference between predicted and actual intents, and optimization techniques, like stochastic gradient descent, are utilized to minimize this loss.
* The training process involves multiple epochs, refining the model's parameters to enhance its predictive accuracy.
* The trained model is saved for later use in the chatbot application.

# How to train your own custom chatbot ?

## Overview of the python files used for this part:
* ntlk_utils.py: contains custom functions
* model.py: contains a class created for the FNN
* train.py: Used to preprocess the intents.json and train the model
* chat.py: This is the file where it utilizes the model generated from training and predicts on user inputs

## Clone repository and create a python virtual environment
```
git clone https://github.com/ongaunjie1/AI-Chatbot-DL-NLP.git
cd AI-Chatbot-DL-NLP
python -m venv venv
venv\Scripts\activate
```
## Install dependencies:
```
(venv) pip install Flask torch torchvision nltk
```
or 
```
(venv) pip install -r requirements.txt
```

## Install nltk package
```
(venv) python
>>> import nltk
>>> nltk.download('punkt')
```
## Modify intents.json with different intents and responses for your Chatbot
* This part is where you can customize your own data

## Model training
```
(venv) python train.py
```
![image](https://github.com/ongaunjie1/AI-Chatbot-DL-NLP/assets/118142884/2c796185-d59e-4f94-ac83-46b18490f93d)

## To start chatting with your chatbot
```
(venv) python chat.py
```
![image](https://github.com/ongaunjie1/AI-Chatbot-DL-NLP/assets/118142884/4cf5c47a-385b-4814-9cd1-fc70d4241008)

## b) Integrating APIs into the chatbot 
* Weather API: fetch real-time weather information based on user queries
* Movie API: fetch movie title's data based on user queries
* For the weather API, use [openweathermap](https://openweathermap.org/api)
* For the movie API, use [themoviedb](https://developer.themoviedb.org/reference/intro/getting-started)
* This requires knowledge on extracting data from APIs, read the documentations for more details

### Refer below for a snippet of how to integrate APIs. NOTE: Add-on the integration within the chat.py file
#### Required library
```
pip install requests
```

```
def weather_details(city):
    api_key = 'INSERT YOUR API KEY HERE'
    country_code = 'MY'
    city_name = city
    search_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={api_key}'

    # Make the API call to search for the movie
    response2 = requests.get(search_url)

    if response2.status_code == 200:
        data = response2.json()
        if len(data) > 0:
            city = data['name']
            temp_celsius = kelvin_to_celsius(data['main']['temp'])
            formatted_celsius = f'{temp_celsius}°C'
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            formatted_humidity = f'{humidity}%'
            wind_speed = data['wind']['speed']
            formatted_wind = f'{wind_speed}m/s'

            city_details = {
                    'city': city,
                    'celsius': formatted_celsius,
                    'description': description,
                    'humidity': formatted_humidity,
                    'Wind Speed': formatted_wind }

            return city_details
        else:
            print(f'No results found for {city}')
    else:
        print(f'Failed to retrieve data for {city}')

    return None
```
* Refer to the chat.py for the movie API implementation and also using the wikipedia library to parse data.
* Upon adding APIs, you will need to create conditional statements (if, elif, else) to help the chatbot differentiate between different types of user queries and trigger specific actions or responses.

### Weather query example:
![image](https://github.com/ongaunjie1/AI-Chatbot-DL-NLP/assets/118142884/2852d30b-0a35-4b9d-b790-b43d3188f86f)

## c) Establishing an API endpoint using the flask framework 
```
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response
import download_nltk_data

app = Flask(__name__)
CORS(app)

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
```

### After creating an end point, you can test it locally to make sure that it works
```
python app.py
```
![image](https://github.com/ongaunjie1/AI-Chatbot-DL-NLP/assets/118142884/65a34032-f38c-480a-928d-5e61463dda88)
* http://127.0.0.1:8000/predict 
* To deploy your chatbot's backend into the cloud. A free option is by using [Render](https://render.com/).

## d) Designing a chatbot user interface for front-end web application
* If you have experience working with front-end frameworks such as CSS, HTML and JavaScript
* You can refer to an chatbot UI made by me within the chatbotui folder.
* Feel free to modify the design to your own liking.
* To test out a live version of the chatbot, check out my portfolio. [Portfolio](https://ongaunjie.com)

### Showcase of the user interface
![image](https://github.com/ongaunjie1/AI-Chatbot-DL-NLP/assets/118142884/161a333c-34b0-4e7e-83d1-6468d9cef9cb)
