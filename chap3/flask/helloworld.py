import os
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def input_form():
    return render_template("input.html")

@app.route('/', methods=['POST'])
def output_form():
    text = request.form['moji']
    return render_template('output.html', moji=text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, threaded=True)
