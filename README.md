# OpenclawControl 🦞

**Live iPhone screen viewer and remote control via WebDriverAgent (WDA)**

Control your iPhone remotely with a 3D animated lobster mascot and live screen preview!

## Features

### 📱 Live iPhone Screen
- Real-time screen mirroring via WebDriverAgent
- Auto-refreshing every 1 second
- iPhone X frame with notch design

### 🦞 3D Lobster Character
- Animated procedural lobster built with Three.js
- **Sleeps when idle** - ZZZ floating animation, closed eyes, lowered claws
- **Click to wake** - Wakes lobster AND triggers iPhone home button
- Full anatomy: eye stalks, antennae, claws with pincers, 8 legs with feet, segmented tail
- Breathing animation when sleeping
- Claw pinching animation when awake

### 🎮 Remote Control Buttons
- **⬆️ Scroll Up / ⬇️ Scroll Down** - Swipe gestures via WDA
- **🏠 Home** - Press home button
- **📸 Screenshot** - Download current screen
- **🦞 Clawd Mode** - Custom automation (placeholder)
- **⏸ Pause / ▶️ Resume** - Control live feed

### 🎨 Modern UI
- Black background with slate grey buttons
- Font Awesome icons
- Clean, minimal design
- Responsive layout

## Prerequisites

### Required
- **iPhone** (jailbroken or with developer account)
- **WebDriverAgent (WDA)** installed and running on iPhone
- **iproxy** - for port forwarding (from libimobiledevice)
- **Python 3.7+**
- **Flask** and **requests** Python packages

### Setup WebDriverAgent
1. Build and install [WebDriverAgent](https://github.com/appium/WebDriverAgent) on your iPhone
2. Start WDA on your iPhone (it should listen on port 8100)
3. Forward the port using iproxy:
   ```bash
   iproxy 8100 8100
   ```

## Installation

```bash
# Clone the repository
git clone https://github.com/kwyatte/OpenclawControl.git
cd OpenclawControl

# Install Python dependencies
pip install flask requests
```

## Usage

1. **Start WebDriverAgent** on your iPhone (via Xcode or other method)

2. **Forward WDA port** using iproxy:
   ```bash
   iproxy 8100 8100
   ```

3. **Run OpenclawControl**:
   ```bash
   python3 wda_viewer.py
   ```

4. **Open in browser**:
   ```
   http://localhost:5000
   ```

5. **Interact**:
   - Watch your iPhone screen in real-time
   - Click the sleeping lobster to wake him and trigger home button
   - Use control buttons to scroll and navigate

## How It Works

### WebDriverAgent Integration
- Connects to WDA running on `localhost:8100` (via iproxy)
- Fetches screenshots via WDA's `/screenshot` endpoint
- Decodes base64 JPEG images from WDA's JSON response
- Sends touch actions via WDA's `/wda/dragfromtoforduration` endpoint
- Triggers home button via WDA's `/wda/homescreen` endpoint

### Architecture
```
iPhone (WDA on port 8100)
    ↓
iproxy (port forwarding)
    ↓
OpenclawControl Flask Server (port 5000)
    ↓
Your Browser (UI + Three.js Lobster)
```

## Controls

- **⬆️ Scroll Up** - Swipe down gesture on iPhone
- **⬇️ Scroll Down** - Swipe up gesture on iPhone
- **🏠 Home** - Press home button
- **📸 Screenshot** - Download current iPhone screen
- **🦞 Clawd Mode** - Custom automation (to be implemented)
- **⏸ Pause** - Stop live screen updates
- **▶️ Resume** - Resume live screen updates
- **🦞 Click Lobster** - Wake lobster and press home button

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **3D Graphics**: Three.js
- **Icons**: Font Awesome
- **iPhone Control**: WebDriverAgent (WDA)
- **Port Forwarding**: iproxy (libimobiledevice)

## Contributing

Contributions welcome! This is an open-source project for iPhone remote control enthusiasts.

## License

Open source - feel free to use and modify!

---

Built with ❤️ using Flask + WebDriverAgent + Three.js

🦞 **OpenclawControl** - Control your iPhone with a lobster!
