#!/usr/bin/env python3
"""
WDA iPhone X Live View
Shows real-time iPhone screen via WebDriverAgent
"""

from flask import Flask, render_template_string, request
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
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
            color: #e2e8f0;
            margin-bottom: 5px;
            font-size: 22px;
            font-weight: 500;
        }

        .status {
            text-align: center;
            color: #64748b;
            font-size: 13px;
            margin-bottom: 20px;
        }

        .status.live {
            color: #10b981;
            font-weight: 500;
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
            cursor: crosshair;
        }

        #screenshot {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .cursor-overlay {
            position: absolute;
            width: 20px;
            height: 20px;
            border: 2px solid #ef4444;
            border-radius: 50%;
            pointer-events: none;
            transform: translate(-50%, -50%);
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 100;
        }

        .cursor-overlay.active {
            opacity: 1;
        }

        .element-inspector {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 15px;
            max-width: 300px;
            max-height: 400px;
            overflow-y: auto;
            display: none;
            z-index: 1000;
        }

        .element-inspector.active {
            display: block;
        }

        .element-inspector h3 {
            color: #e2e8f0;
            font-size: 14px;
            margin-bottom: 10px;
        }

        .element-inspector pre {
            color: #94a3b8;
            font-size: 11px;
            white-space: pre-wrap;
            word-break: break-all;
        }

        .text-input-bar {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }

        .text-input-bar input {
            flex: 1;
            padding: 8px 12px;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 6px;
            color: #e2e8f0;
            font-size: 14px;
        }

        .text-input-bar input:focus {
            outline: none;
            border-color: #3b82f6;
        }

        .gesture-mode {
            margin-top: 10px;
            text-align: center;
            color: #64748b;
            font-size: 12px;
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
            padding: 14px 20px;
            background: #1e293b;
            color: #e2e8f0;
            border: 1px solid #334155;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        button:hover {
            background: #334155;
            border-color: #475569;
        }

        button:active {
            transform: translateY(1px);
        }

        .btn-primary {
            background: #3b82f6;
            border-color: #3b82f6;
        }

        .btn-primary:hover {
            background: #2563eb;
            border-color: #2563eb;
        }

        .btn-success {
            background: #10b981;
            border-color: #10b981;
        }

        .btn-success:hover {
            background: #059669;
            border-color: #059669;
        }

        .btn-danger {
            background: #ef4444;
            border-color: #ef4444;
        }

        .btn-danger:hover {
            background: #dc2626;
            border-color: #dc2626;
        }

        .refresh-rate {
            text-align: center;
            margin-top: 15px;
            color: #64748b;
            font-size: 12px;
        }

        .error {
            color: #ef4444;
            text-align: center;
            padding: 10px;
            font-size: 13px;
        }

        button i {
            font-size: 14px;
        }

        #lobster-container {
            width: 100%;
            height: 300px;
            margin-top: 20px;
            border-radius: 8px;
            overflow: hidden;
            cursor: pointer;
            background: #000;
            border: 1px solid #334155;
        }

        #lobster-container:hover {
            border-color: #ef4444;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="phone-section">
            <h1><i class="fa-solid fa-mobile-screen"></i> iPhone X Live View</h1>
            <div class="status" id="status">Connecting to WDA...</div>

            <div class="iphone-x">
            <div class="notch">
                <div class="camera"></div>
                <div class="speaker"></div>
            </div>
            <div class="screen">
                <div class="screen-content" id="screenContent">
                    <div class="loading" id="loading">
                        <div class="spinner"></div>
                        Loading screen...
                    </div>
                    <img id="screenshot" style="display: none;" alt="iPhone Screen">
                    <div class="cursor-overlay" id="cursor"></div>
                </div>
            </div>
        </div>
        </div>

        <div class="controls-section">
            <div class="controls">
                <div class="control-group">
                    <button onclick="scrollUp()"><i class="fa-solid fa-arrow-up"></i> Scroll Up</button>
                    <button onclick="scrollDown()"><i class="fa-solid fa-arrow-down"></i> Scroll Down</button>
                </div>
                <div class="control-group">
                    <button class="btn-primary" onclick="goHome()"><i class="fa-solid fa-house"></i> Home</button>
                    <button onclick="takeScreenshot()"><i class="fa-solid fa-camera"></i> Screenshot</button>
                </div>
                <div class="control-group">
                    <button class="btn-danger" onclick="clawdMode()">🦞 Clawd Mode</button>
                </div>
                <div class="control-group">
                    <button onclick="pauseRefresh()"><i class="fa-solid fa-pause"></i> Pause</button>
                    <button onclick="resumeRefresh()"><i class="fa-solid fa-play"></i> Resume</button>
                </div>
            </div>

            <div class="refresh-rate">Auto-refresh: <span id="rate">1s</span></div>
            <div class="gesture-mode">Mode: <span id="gestureMode">Tap</span> | Hold Shift: Long Press | Hold Ctrl: Inspect</div>
            <div class="error" id="error" style="display: none;"></div>

            <div class="text-input-bar">
                <input type="text" id="textInput" placeholder="Type text to send to iPhone...">
                <button onclick="sendText()"><i class="fa-solid fa-keyboard"></i> Send</button>
            </div>

            <div id="lobster-container"></div>
        </div>

        <div class="element-inspector" id="inspector">
            <h3><i class="fa-solid fa-magnifying-glass"></i> Element Inspector</h3>
            <pre id="inspectorContent">Click element while holding Ctrl...</pre>
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

        function sendText() {
            const input = document.getElementById('textInput');
            const text = input.value;
            if (!text) return;

            fetch('/wda/type', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            }).then(r => r.json()).then(data => {
                console.log('Text sent:', data);
                input.value = '';
            });
        }

        // Remote control functionality
        const screenContent = document.getElementById('screenContent');
        const cursor = document.getElementById('cursor');
        const screenshot = document.getElementById('screenshot');
        const inspector = document.getElementById('inspector');
        const inspectorContent = document.getElementById('inspectorContent');
        const gestureModeLabel = document.getElementById('gestureMode');

        let touchStartTime = 0;
        let touchStartPos = {x: 0, y: 0};

        // Convert browser coordinates to iPhone coordinates
        function convertCoords(event) {
            const rect = screenshot.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            // iPhone X resolution: 1125x2436 (3x scale of 375x812)
            const iPhoneX = Math.round((x / rect.width) * 375);
            const iPhoneY = Math.round((y / rect.height) * 812);

            return {x: iPhoneX, y: iPhoneY, browserX: x, browserY: y};
        }

        // Show cursor on hover
        screenContent.addEventListener('mousemove', (e) => {
            if (e.target !== screenshot) return;
            const coords = convertCoords(e);
            cursor.style.left = coords.browserX + 'px';
            cursor.style.top = coords.browserY + 'px';
            cursor.classList.add('active');
        });

        screenContent.addEventListener('mouseleave', () => {
            cursor.classList.remove('active');
        });

        // Handle clicks/taps
        screenContent.addEventListener('mousedown', (e) => {
            if (e.target !== screenshot) return;
            e.preventDefault();

            touchStartTime = Date.now();
            const coords = convertCoords(e);
            touchStartPos = coords;

            // Update gesture mode display
            if (e.shiftKey) {
                gestureModeLabel.textContent = 'Long Press';
            } else if (e.ctrlKey || e.metaKey) {
                gestureModeLabel.textContent = 'Inspect';
            } else {
                gestureModeLabel.textContent = 'Tap';
            }
        });

        screenContent.addEventListener('mouseup', (e) => {
            if (e.target !== screenshot) return;
            e.preventDefault();

            const duration = (Date.now() - touchStartTime) / 1000;
            const coords = convertCoords(e);
            const distance = Math.sqrt(
                Math.pow(coords.x - touchStartPos.x, 2) +
                Math.pow(coords.y - touchStartPos.y, 2)
            );

            // Inspect mode (Ctrl/Cmd + Click)
            if (e.ctrlKey || e.metaKey) {
                inspector.classList.add('active');
                inspectorContent.textContent = 'Loading element info...';

                fetch('/wda/source')
                    .then(r => r.json())
                    .then(data => {
                        inspectorContent.textContent = JSON.stringify(data, null, 2);
                    })
                    .catch(err => {
                        inspectorContent.textContent = 'Error: ' + err;
                    });
                return;
            }

            // Long press (Shift + Click or hold > 0.5s)
            if (e.shiftKey || duration > 0.5) {
                fetch('/wda/longpress', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({x: coords.x, y: coords.y, duration: 1.0})
                }).then(r => r.json()).then(data => {
                    console.log('Long press:', data);
                });
                return;
            }

            // Swipe (moved > 10 pixels)
            if (distance > 10) {
                fetch('/wda/scroll', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        direction: coords.y < touchStartPos.y ? 'down' : 'up'
                    })
                }).then(r => r.json()).then(data => {
                    console.log('Swipe:', data);
                });
                return;
            }

            // Regular tap
            fetch('/wda/tap', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({x: coords.x, y: coords.y})
            }).then(r => r.json()).then(data => {
                console.log('Tap:', data);
            });

            gestureModeLabel.textContent = 'Tap';
        });

        // Close inspector
        inspector.addEventListener('click', () => {
            inspector.classList.remove('active');
        });

        // Text input on Enter
        document.getElementById('textInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendText();
            }
        });

        function clawdMode() {
            fetch('/wda/clawd', {
                method: 'POST'
            }).then(r => r.json()).then(data => {
                console.log('Clawd Mode:', data);
                alert('Clawd Mode activated!');
            });
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

        // Three.js Lobster
        const container = document.getElementById('lobster-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x000000);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 1, 5);
        camera.lookAt(0, 0.5, 0);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);
        const pointLight = new THREE.PointLight(0xef4444, 1);
        pointLight.position.set(5, 5, 5);
        scene.add(pointLight);

        // Create detailed lobster character
        const lobster = new THREE.Group();
        const red = new THREE.MeshPhongMaterial({ color: 0xef4444, shininess: 30 });
        const darkRed = new THREE.MeshPhongMaterial({ color: 0xdc2626, shininess: 30 });
        const eyeWhite = new THREE.MeshPhongMaterial({ color: 0xffffff, shininess: 100 });
        const eyeBlack = new THREE.MeshPhongMaterial({ color: 0x000000 });

        // Main Body (torso)
        const body = new THREE.Mesh(new THREE.SphereGeometry(0.5, 32, 32), red);
        body.scale.set(1, 1.3, 0.9);
        body.position.y = 0.4;
        lobster.add(body);

        // Head/Face
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 32, 32), red);
        head.position.y = 1.1;
        lobster.add(head);

        // Eye stalks
        const leftEyeStalk = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.2, 8), red);
        leftEyeStalk.position.set(-0.15, 1.35, 0.2);
        leftEyeStalk.rotation.x = Math.PI / 6;
        lobster.add(leftEyeStalk);

        const rightEyeStalk = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.2, 8), red);
        rightEyeStalk.position.set(0.15, 1.35, 0.2);
        rightEyeStalk.rotation.x = Math.PI / 6;
        lobster.add(rightEyeStalk);

        // Eyes
        const leftEye = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 16), eyeWhite);
        leftEye.position.set(-0.15, 1.45, 0.28);
        lobster.add(leftEye);

        const leftPupil = new THREE.Mesh(new THREE.SphereGeometry(0.05, 16, 16), eyeBlack);
        leftPupil.position.set(-0.15, 1.45, 0.35);
        lobster.add(leftPupil);

        const rightEye = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 16), eyeWhite);
        rightEye.position.set(0.15, 1.45, 0.28);
        lobster.add(rightEye);

        const rightPupil = new THREE.Mesh(new THREE.SphereGeometry(0.05, 16, 16), eyeBlack);
        rightPupil.position.set(0.15, 1.45, 0.35);
        lobster.add(rightPupil);

        // Antennae
        const leftAntenna = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.4, 8), darkRed);
        leftAntenna.position.set(-0.25, 1.5, 0.15);
        leftAntenna.rotation.z = -Math.PI / 6;
        leftAntenna.rotation.x = Math.PI / 8;
        lobster.add(leftAntenna);

        const rightAntenna = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.4, 8), darkRed);
        rightAntenna.position.set(0.25, 1.5, 0.15);
        rightAntenna.rotation.z = Math.PI / 6;
        rightAntenna.rotation.x = Math.PI / 8;
        lobster.add(rightAntenna);

        // Big Claws (arms + pincers)
        // Left claw arm
        const leftClawArm = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.5, 16), darkRed);
        leftClawArm.position.set(-0.55, 0.6, 0.1);
        leftClawArm.rotation.z = -Math.PI / 4;
        lobster.add(leftClawArm);

        // Left claw hand
        const leftClaw = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.2, 0.3), darkRed);
        leftClaw.position.set(-0.85, 0.35, 0.1);
        lobster.add(leftClaw);

        // Left claw pincer top
        const leftPincerTop = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.05, 0.15), darkRed);
        leftPincerTop.position.set(-1.05, 0.42, 0.1);
        lobster.add(leftPincerTop);

        // Right claw arm
        const rightClawArm = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.5, 16), darkRed);
        rightClawArm.position.set(0.55, 0.6, 0.1);
        rightClawArm.rotation.z = Math.PI / 4;
        lobster.add(rightClawArm);

        // Right claw hand
        const rightClaw = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.2, 0.3), darkRed);
        rightClaw.position.set(0.85, 0.35, 0.1);
        lobster.add(rightClaw);

        // Right claw pincer top
        const rightPincerTop = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.05, 0.15), darkRed);
        rightPincerTop.position.set(1.05, 0.42, 0.1);
        lobster.add(rightPincerTop);

        // Walking Legs (4 pairs = 8 legs)
        const legGeometry = new THREE.CylinderGeometry(0.04, 0.03, 0.5, 8);

        for (let i = 0; i < 4; i++) {
            // Left legs
            const leftLeg = new THREE.Mesh(legGeometry, darkRed);
            leftLeg.position.set(-0.4, -0.15, 0.15 - i * 0.15);
            leftLeg.rotation.z = -Math.PI / 5;
            lobster.add(leftLeg);

            // Left foot
            const leftFoot = new THREE.Mesh(new THREE.SphereGeometry(0.04, 8, 8), darkRed);
            leftFoot.position.set(-0.62, -0.4, 0.15 - i * 0.15);
            lobster.add(leftFoot);

            // Right legs
            const rightLeg = new THREE.Mesh(legGeometry, darkRed);
            rightLeg.position.set(0.4, -0.15, 0.15 - i * 0.15);
            rightLeg.rotation.z = Math.PI / 5;
            lobster.add(rightLeg);

            // Right foot
            const rightFoot = new THREE.Mesh(new THREE.SphereGeometry(0.04, 8, 8), darkRed);
            rightFoot.position.set(0.62, -0.4, 0.15 - i * 0.15);
            lobster.add(rightFoot);
        }

        // Tail segments
        const tail1 = new THREE.Mesh(new THREE.SphereGeometry(0.3, 16, 16), red);
        tail1.scale.set(0.8, 1, 1);
        tail1.position.set(0, 0.1, -0.45);
        lobster.add(tail1);

        const tail2 = new THREE.Mesh(new THREE.SphereGeometry(0.25, 16, 16), red);
        tail2.scale.set(0.7, 0.9, 1);
        tail2.position.set(0, -0.05, -0.7);
        lobster.add(tail2);

        const tailFan = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.02, 0.3), darkRed);
        tailFan.position.set(0, -0.1, -0.85);
        lobster.add(tailFan);

        lobster.position.y = -0.3;
        scene.add(lobster);

        // Add ZZZ text sprites for sleeping
            const canvas = document.createElement('canvas');
        canvas.width = 128;
        canvas.height = 128;
        const ctx = canvas.getContext('2d');
        ctx.font = 'bold 80px Arial';
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText('Z', 64, 80);

        const texture = new THREE.CanvasTexture(canvas);
        const spriteMaterial = new THREE.SpriteMaterial({ map: texture, transparent: true });

        const zzz1 = new THREE.Sprite(spriteMaterial);
        zzz1.scale.set(0.3, 0.3, 1);
        zzz1.position.set(1, 2.5, 0);
        zzz1.visible = false;
        lobster.add(zzz1);

        const zzz2 = new THREE.Sprite(spriteMaterial);
        zzz2.scale.set(0.25, 0.25, 1);
        zzz2.position.set(1.2, 3, 0);
        zzz2.visible = false;
        lobster.add(zzz2);

        const zzz3 = new THREE.Sprite(spriteMaterial);
        zzz3.scale.set(0.2, 0.2, 1);
        zzz3.position.set(1.4, 3.5, 0);
        zzz3.visible = false;
        lobster.add(zzz3);

        // Animation state
        let isAwake = false;
        let sleepTime = 0;

        // Sleeping animation
        function sleep() {
            isAwake = false;
            head.rotation.x = -0.4;
            lobster.position.y = -0.8;
            leftEye.scale.y = 0.1;
            rightEye.scale.y = 0.1;
            leftPupil.visible = false;
            rightPupil.visible = false;
            leftClaw.position.y = 0.2;
            rightClaw.position.y = 0.2;
            zzz1.visible = true;
            zzz2.visible = true;
            zzz3.visible = true;
        }

        // Wake up animation
        function wakeUp() {
            isAwake = true;
            head.rotation.x = 0;
            lobster.position.y = -0.5;
            leftEye.scale.y = 1;
            rightEye.scale.y = 1;
            leftPupil.visible = true;
            rightPupil.visible = true;
            leftClaw.position.y = 0.5;
            rightClaw.position.y = 0.5;
            zzz1.visible = false;
            zzz2.visible = false;
            zzz3.visible = false;
            setTimeout(() => { lobster.position.y = -0.2; }, 100);
            setTimeout(() => { lobster.position.y = -0.5; }, 300);
        }

        // Start sleeping
        sleep();

        // Click handler
        container.addEventListener('click', () => {
            if (!isAwake) {
                wakeUp();
                goHome();
            }
        });

        // Animation loop
        function animate() {
            requestAnimationFrame(animate);

            if (isAwake) {
                lobster.position.y = -0.5 + Math.sin(Date.now() * 0.001) * 0.05;
                leftClaw.scale.x = 1 + Math.sin(Date.now() * 0.003) * 0.1;
                rightClaw.scale.x = 1 + Math.sin(Date.now() * 0.003 + Math.PI) * 0.1;
            } else {
                body.scale.y = 1.2 + Math.sin(Date.now() * 0.0005) * 0.05;
                sleepTime += 0.01;
                zzz1.position.y = 1.5 + Math.sin(sleepTime) * 0.3;
                zzz2.position.y = 2 + Math.sin(sleepTime + 1) * 0.3;
                zzz3.position.y = 2.5 + Math.sin(sleepTime + 2) * 0.3;
                zzz1.material.opacity = 0.5 + Math.sin(sleepTime) * 0.3;
                zzz2.material.opacity = 0.5 + Math.sin(sleepTime + 1) * 0.3;
                zzz3.material.opacity = 0.5 + Math.sin(sleepTime + 2) * 0.3;
            }

            renderer.render(scene, camera);
        }
        animate();

        // Window resize
        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
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

@app.route('/wda/clawd', methods=['POST'])
def wda_clawd():
    """Clawd Mode - placeholder for custom automation"""
    try:
        # TODO: Implement Clawd Mode automation
        return {'status': 'success', 'message': 'Clawd Mode activated'}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/wda/tap', methods=['POST'])
def wda_tap():
    """Tap at coordinates on iPhone screen"""
    try:
        data = request.json
        x = data.get('x', 0)
        y = data.get('y', 0)

        # First ensure we have a session
        session_response = requests.post(
            'http://localhost:8100/session',
            json={'capabilities': {}},
            timeout=5
        )
        session_id = session_response.json().get('sessionId')

        # Use W3C WebDriver actions endpoint
        tap_data = {
            "actions": [{
                "type": "pointer",
                "id": "finger1",
                "parameters": {"pointerType": "touch"},
                "actions": [
                    {"type": "pointerMove", "duration": 0, "x": x, "y": y},
                    {"type": "pointerDown"},
                    {"type": "pause", "duration": 100},
                    {"type": "pointerUp"}
                ]
            }]
        }
        response = requests.post(
            f'http://localhost:8100/session/{session_id}/actions',
            json=tap_data,
            timeout=5
        )
        return response.json(), response.status_code
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/wda/longpress', methods=['POST'])
def wda_longpress():
    """Long press at coordinates"""
    try:
        data = request.json
        x = data.get('x', 0)
        y = data.get('y', 0)
        duration = data.get('duration', 1.0)

        # First ensure we have a session
        session_response = requests.post(
            'http://localhost:8100/session',
            json={'capabilities': {}},
            timeout=5
        )
        session_id = session_response.json().get('sessionId')

        # Use W3C WebDriver actions endpoint for long press
        press_data = {
            "actions": [{
                "type": "pointer",
                "id": "finger1",
                "parameters": {"pointerType": "touch"},
                "actions": [
                    {"type": "pointerMove", "duration": 0, "x": x, "y": y},
                    {"type": "pointerDown"},
                    {"type": "pause", "duration": int(duration * 1000)},  # Convert to milliseconds
                    {"type": "pointerUp"}
                ]
            }]
        }
        response = requests.post(
            f'http://localhost:8100/session/{session_id}/actions',
            json=press_data,
            timeout=5
        )
        return response.json(), response.status_code
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/wda/source', methods=['GET'])
def wda_source():
    """Get accessibility hierarchy (element tree)"""
    try:
        response = requests.get('http://localhost:8100/source', timeout=10)
        return response.json(), response.status_code
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/wda/type', methods=['POST'])
def wda_type():
    """Type text on iOS keyboard"""
    try:
        data = request.json
        text = data.get('text', '')

        # Use WDA keys endpoint
        response = requests.post(
            'http://localhost:8100/wda/keys',
            json={'value': list(text)},
            timeout=5
        )
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
