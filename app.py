from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
from chatbot import response

app = Flask(__name__)


# port = 5000

@app.route('/')  # homepage
def index_get():
    return render_template('base.html')


@app.route('/predict', methods=['POST'])
def predict():
    text = request.get_json().get(
        'message')  # the input which user will give will get called by request.get_json function and get stored in text variable
    response1 = response(
        text)  # the function we created response has our model to compute this response we will get from user in text variable and classify it and give respective output
    message = {'answer': response1}
    return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True)  # (host="0.0.0.0", port=port, debug=True)

# When we run flask file if we are getting 200/304 at the end that means it has no error else if we getting 404 so before that whatever file is there or
# line we have to check that line in code to resolve it
