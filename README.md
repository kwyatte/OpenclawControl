# iOS Remote

Live iPhone screen viewer and remote control via WebDriverAgent (WDA).

## Features

- 📱 Real-time iPhone screen display
- 🎮 Remote control buttons:
  - Scroll Up/Down
  - Home button
  - Screenshot download
  - Pause/Resume live feed
- ⚡ Auto-refreshing every 1 second
- 🌑 Dark theme interface

## Prerequisites

- iPhone with WebDriverAgent installed
- `iproxy` running: `iproxy 8100 8100`
- Python 3.7+
- Flask
- requests

## Installation

```bash
pip install flask requests
```

## Usage

1. Start iproxy to forward WDA port:
```bash
iproxy 8100 8100
```

2. Run the viewer:
```bash
python3 wda_viewer.py
```

3. Open in browser:
```
http://localhost:5000
```

## How It Works

- Connects to WebDriverAgent on port 8100
- Fetches screenshots via WDA's `/screenshot` endpoint
- Decodes base64 JPEG images
- Sends touch actions for scrolling and home button
- Updates display every second for live view

## Controls

- **⬆️ Scroll Up** - Swipe down gesture
- **⬇️ Scroll Down** - Swipe up gesture
- **🏠 Home** - Press home button
- **📸 Screenshot** - Download current screen
- **⏸ Pause** - Stop live updates
- **▶️ Resume** - Resume live updates

---

Built with Flask + WebDriverAgent
