#!/usr/bin/env python3
"""
WDA iPhone X Live View
Shows real-time iPhone screen via WebDriverAgent
"""

from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# WDA Screenshot endpoint
WDA_URL = "http://localhost:8100/screenshot"

VIEWER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>iPhone X Live View</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #000;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: #000;
            border-radius: 30px;
            padding: 30px;
            max-width: 900px;
            display: flex;
            gap: 40px;
            align-items: center;
        }

        .phone-section {
            flex-shrink: 0;
        }

        .controls-section {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        h1 {
            text-align: center;
            color: #fff;
            margin-bottom: 5px;
            font-size: 24px;
        }

        .status {
            text-align: center;
            color: #999;
            font-size: 13px;
            margin-bottom: 20px;
        }

        .status.live {
            color: #00ff00;
            font-weight: 600;
        }

        /* iPhone X Frame */
        .iphone-x {
            position: relative;
            width: 360px;
            height: 720px;
            margin: 0 auto;
            background: #1a1a1a;
            border-radius: 45px;
            padding: 12px;
            box-shadow:
                0 0 0 2px #2a2a2a,
                0 0 0 6px #1a1a1a,
                0 20px 50px rgba(0, 0, 0, 0.5);
        }

        /* Notch */
        .notch {
            position: absolute;
            top: 12px;
            left: 50%;
            transform: translateX(-50%);
            width: 210px;
            height: 30px;
            background: #1a1a1a;
            border-radius: 0 0 20px 20px;
            z-index: 10;
        }

        .camera {
            position: absolute;
            right: 70px;
            top: 8px;
            width: 12px;
            height: 12px;
            background: #0a0a0a;
            border-radius: 50%;
            box-shadow: inset 0 0 3px rgba(100, 150, 255, 0.8);
        }

        .speaker {
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            top: 11px;
            width: 60px;
            height: 6px;
            background: #0a0a0a;
            border-radius: 3px;
        }

        /* Screen */
        .screen {
            position: relative;
            width: 100%;
            height: 100%;
            background: #000;
            border-radius: 35px;
            overflow: hidden;
        }

        .screen-content {
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f0f0f0;
        }

        #screenshot {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #999;
            font-size: 14px;
            text-align: center;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #e0e0e0;
            border-top-color: #1e3c72;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .controls {
            display: flex;
            flex-direction: column;
            gap: 15px;
            width: 100%;
        }

        .control-group {
            display: flex;
            gap: 10px;
            width: 100%;
        }

        button {
            padding: 15px 20px;
            background: #1a1a1a;
            color: #0f0;
            border: 2px solid #0f0;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-family: monospace;
            flex: 1;
        }

        button:hover {
            background: #0f0;
            color: #000;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
        }

        button:active {
            transform: scale(0.95);
        }

        .btn-action {
            background: #1a1a1a;
            border-color: #00ffff;
            color: #00ffff;
        }

        .btn-action:hover {
            background: #00ffff;
            color: #000;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        }

        .refresh-rate {
            text-align: center;
            margin-top: 15px;
            color: #666;
            font-size: 12px;
        }

        .error {
            color: #d32f2f;
            text-align: center;
            padding: 10px;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="phone-section">
            <h1>📱 iPhone X Live View</h1>
            <div class="status" id="status">Connecting to WDA...</div>

            <div class="iphone-x">
            <div class="notch">
                <div class="camera"></div>
                <div class="speaker"></div>
            </div>
            <div class="screen">
                <div class="screen-content">
                    <div class="loading" id="loading">
                        <div class="spinner"></div>
                        Loading screen...
                    </div>
                    <img id="screenshot" style="display: none;" alt="iPhone Screen">
                </div>
            </div>
        </div>
        </div>

        <div class="controls-section">
            <div class="controls">
                <div class="control-group">
                    <button onclick="scrollUp()">⬆️ Scroll Up</button>
                    <button onclick="scrollDown()">⬇️ Scroll Down</button>
                </div>
                <div class="control-group">
                    <button class="btn-action" onclick="goHome()">🏠 Home</button>
                    <button class="btn-action" onclick="takeScreenshot()">📸 Screenshot</button>
                </div>
                <div class="control-group">
                    <button onclick="pauseRefresh()">⏸ Pause</button>
                    <button onclick="resumeRefresh()">▶️ Resume</button>
                </div>
            </div>

            <div class="refresh-rate">Auto-refresh: <span id="rate">1s</span></div>
            <div class="error" id="error" style="display: none;"></div>
        </div>
    </div>

    <script>
        let refreshInterval;
        let isPaused = false;
        const img = document.getElementById('screenshot');
        const loading = document.getElementById('loading');
        const status = document.getElementById('status');
        const errorDiv = document.getElementById('error');

        function updateScreenshot() {
            if (isPaused) return;

            // Add timestamp to prevent caching
            const timestamp = new Date().getTime();
            const url = '/wda/screenshot?t=' + timestamp;

            fetch(url)
                .then(response => {
                    if (!response.ok) throw new Error('WDA connection failed');
                    return response.blob();
                })
                .then(blob => {
                    const imageUrl = URL.createObjectURL(blob);
                    img.onload = function() {
                        loading.style.display = 'none';
                        img.style.display = 'block';
                        status.textContent = '🟢 Live';
                        status.className = 'status live';
                        errorDiv.style.display = 'none';
                    };
                    img.src = imageUrl;
                })
                .catch(error => {
                    console.error('Screenshot error:', error);
                    status.textContent = '🔴 Disconnected';
                    status.className = 'status';
                    errorDiv.textContent = 'Cannot connect to WDA on port 8100. Make sure iproxy is running.';
                    errorDiv.style.display = 'block';
                });
        }

        function pauseRefresh() {
            isPaused = true;
            status.textContent = '⏸ Paused';
            status.className = 'status';
        }

        function resumeRefresh() {
            isPaused = false;
            status.textContent = '🟢 Live';
            status.className = 'status live';
            updateScreenshot();
        }

        function refreshNow() {
            isPaused = false;
            updateScreenshot();
        }

        function scrollUp() {
            fetch('/wda/scroll', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({direction: 'up'})
            }).then(r => r.json()).then(data => {
                console.log('Scroll up:', data);
            });
        }

        function scrollDown() {
            fetch('/wda/scroll', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({direction: 'down'})
            }).then(r => r.json()).then(data => {
                console.log('Scroll down:', data);
            });
        }

        function goHome() {
            fetch('/wda/home', {
                method: 'POST'
            }).then(r => r.json()).then(data => {
                console.log('Home button:', data);
            });
        }

        function takeScreenshot() {
            const link = document.createElement('a');
            link.href = '/wda/screenshot';
            link.download = 'iphone_screenshot_' + Date.now() + '.jpg';
            link.click();
        }

        // Start auto-refresh
        updateScreenshot();
        refreshInterval = setInterval(updateScreenshot, 1000); // Update every 1 second

        // Cleanup old blob URLs to prevent memory leaks
        let lastUrl = null;
        img.addEventListener('load', function() {
            if (lastUrl) {
                URL.revokeObjectURL(lastUrl);
            }
            lastUrl = img.src;
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(VIEWER_HTML)

@app.route('/wda/screenshot')
def wda_screenshot():
    """Proxy WDA screenshot endpoint - decode base64 JSON response"""
    try:
        response = requests.get(WDA_URL, timeout=5)
        if response.status_code == 200:
            import base64
            data = response.json()
            # WDA returns {"value": {"screenshot": "base64_data"}, "sessionId": "..."}
            img_base64 = data.get('value', {}).get('screenshot', '')
            if not img_base64:
                return "No screenshot data in response", 500
            img_bytes = base64.b64decode(img_base64)
            return img_bytes, 200, {'Content-Type': 'image/png'}
        else:
            return f"WDA error: {response.status_code}", response.status_code
    except Exception as e:
        return str(e), 500

@app.route('/wda/home', methods=['POST'])
def wda_home():
    """Press home button via WDA"""
    try:
        response = requests.post('http://localhost:8100/wda/homescreen', timeout=5)
        return response.json(), response.status_code
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/wda/scroll', methods=['POST'])
def wda_scroll():
    """Scroll screen via WDA swipe/drag API"""
    try:
        from flask import request
        data = request.json
        direction = data.get('direction', 'down')

        # iPhone screen dimensions (approximate for iPhone X)
        screen_width = 375
        screen_height = 812
        center_x = screen_width // 2

        # Define swipe coordinates based on direction
        if direction == 'down':
            # Swipe down = scroll up content
            from_y = int(screen_height * 0.7)
            to_y = int(screen_height * 0.3)
        else:  # up
            # Swipe up = scroll down content
            from_y = int(screen_height * 0.3)
            to_y = int(screen_height * 0.7)

        # Use WDA drag/swipe endpoint
        swipe_data = {
            "fromX": center_x,
            "fromY": from_y,
            "toX": center_x,
            "toY": to_y,
            "duration": 0.3
        }

        # Try the /wda/dragfromtoforduration endpoint
        response = requests.post(
            'http://localhost:8100/wda/dragfromtoforduration',
            json=swipe_data,
            timeout=5
        )

        if response.status_code != 200:
            # Fallback: try session-based swipe
            # First get session
            session_resp = requests.get('http://localhost:8100/status', timeout=5)
            if session_resp.status_code == 200:
                session_id = session_resp.json().get('sessionId', '')
                if session_id:
                    # Use session-based touch action
                    actions_data = {
                        "actions": [{
                            "type": "pointer",
                            "id": "finger1",
                            "parameters": {"pointerType": "touch"},
                            "actions": [
                                {"type": "pointerMove", "duration": 0, "x": center_x, "y": from_y},
                                {"type": "pointerDown", "button": 0},
                                {"type": "pause", "duration": 100},
                                {"type": "pointerMove", "duration": 300, "x": center_x, "y": to_y},
                                {"type": "pointerUp", "button": 0}
                            ]
                        }]
                    }
                    response = requests.post(
                        f'http://localhost:8100/session/{session_id}/actions',
                        json=actions_data,
                        timeout=5
                    )

        return response.json(), response.status_code
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    print("🦞 WDA iPhone X Live View")
    print("=" * 50)
    print("📱 Connecting to WebDriverAgent on port 8100...")
    print("🌐 Server running on http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False)
