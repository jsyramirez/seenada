from flask import Flask

app = Flask(__name__)

# basic homepage
@app.route('/')
def home():
    return "Welcome to the page"

if __name__ == '__main__':
    app.run(host='0.0.0.0')

