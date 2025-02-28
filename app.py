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
    app.run(debug=True, port=8000)


    


