from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    return f"""
    <html>
        <head><title>GKE App</title></head>
        <body>
            <h1>Hello from GKE!</h1>
            <p>Host: {hostname}</p>
            <p>Version: 1.0</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)