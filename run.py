from market import app
from flask import Flask
import os

@app.route('/')
def home():
    return "Hello from Flask!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

