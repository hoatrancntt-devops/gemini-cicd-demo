from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Jenkins - Harbor - ArgoCD Pipeline!-V11111111111"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
