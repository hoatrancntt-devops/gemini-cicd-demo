from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello():
    return "-Vanhoa-------Hello from Jenkins - Harbor - ArgoCD Pipeline!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
