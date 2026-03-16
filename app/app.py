from flask import Flask, jsonify, request
import socket
import os
import datetime
import platform
import requests

app = Flask(__name__)

# Get pod name from environment (set by Kubernetes)
POD_NAME = socket.gethostname()

@app.route('/')
def home():
    """Main landing page with beautiful styling"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 GKE CI/CD Platform</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px;
                margin: 0;
                min-height: 100vh;
            }}
            .container {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                max-width: 800px;
                margin: 0 auto;
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            }}
            h1 {{
                font-size: 3em;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            .pod-info {{
                background: rgba(255,255,255,0.2);
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                font-size: 1.2em;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-card {{
                background: rgba(255,255,255,0.15);
                border-radius: 10px;
                padding: 20px;
                transition: transform 0.3s;
            }}
            .stat-card:hover {{
                transform: translateY(-5px);
                background: rgba(255,255,255,0.25);
            }}
            .badge {{
                display: inline-block;
                background: #4CAF50;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
                margin: 5px;
            }}
            .footer {{
                margin-top: 40px;
                font-size: 0.9em;
                opacity: 0.8;
            }}
            .success {{
                color: #4CAF50;
                font-weight: bold;
            }}
            .timestamp {{
                font-family: monospace;
                font-size: 1.1em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Welcome to GKE CI/CD Platform</h1>
            
            <div class="pod-info">
                <h3>📦 Pod Information</h3>
                <p><strong>Hostname:</strong> <code>{POD_NAME}</code></p>
                <p><strong>Version:</strong> <span class="badge">1.0</span></p>
                <p><strong>Status:</strong> <span class="success">✅ Running</span></p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>📊 Uptime</h3>
                    <p class="timestamp">{get_uptime()}</p>
                </div>
                <div class="stat-card">
                    <h3>🐍 Python</h3>
                    <p>{platform.python_version()}</p>
                </div>
                <div class="stat-card">
                    <h3>🕒 Server Time</h3>
                    <p class="timestamp">{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>📡 Platform</h3>
                    <p>{platform.platform()}</p>
                </div>
                <div class="stat-card">
                    <h3>🔧 Processor</h3>
                    <p>{platform.processor() or 'Unknown'}</p>
                </div>
                <div class="stat-card">
                    <h3>💾 Environment</h3>
                    <p>GKE</p>
                </div>
            </div>
            
            <div class="footer">
                <p>🚀 Deployed via Jenkins CI/CD Pipeline | 📦 Running on Google Kubernetes Engine</p>
                <p>💻 Container: {POD_NAME} | 🔄 Last Deployed: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes probes"""
    return jsonify({
        'status': 'healthy',
        'pod': POD_NAME,
        'timestamp': datetime.datetime.now().isoformat()
    }), 200

@app.route('/info')
def info():
    """Detailed pod information endpoint"""
    return jsonify({
        'pod_name': POD_NAME,
        'version': '1.0',
        'python_version': platform.python_version(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'hostname': socket.gethostname(),
        'environment': 'GKE',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/echo/<message>')
def echo(message):
    """Echo endpoint for testing"""
    return jsonify({
        'message': message,
        'pod': POD_NAME,
        'length': len(message)
    })

def get_uptime():
    """Get container uptime"""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    except:
        return "N/A"

@app.errorhandler(404)
def not_found(e):
    """Custom 404 page"""
    return jsonify({
        'error': 'Route not found',
        'pod': POD_NAME,
        'message': 'Try /, /health, /info, or /echo/something'
    }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)