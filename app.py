from flask import Flask, request, jsonify
from system import predict_class, get_response
from intents import intents
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['MAX_FILES'] = 1000

@app.route('/')
@app.route('/api/chatbot', methods=['GET', 'POST'])
def chatbot():
    data = request.get_json()
    message = data['message']
    ints = predict_class(message)
    res = get_response(ints, intents)
    print(res)
    return jsonify({'response': res})

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/upload', methods=['POST'])
def upload():
    allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    files = request.files.getlist('file')
    filtered_files = []
    for file in files:
        if file.filename.split('.')[-1].lower() in allowed_extensions:
            filtered_files.append(file)
    # save the filtered_files to disk or process them in some way
    return 'Files uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    