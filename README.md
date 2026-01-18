# Video Call Application

A complete WebRTC-based video calling application using Flask, Socket.IO, and TURN/STUN servers for remote connectivity.

## Features

- Real-time video and audio calling
- Remote connectivity using TURN/STUN servers
- Room-based calling system
- Mute/unmute microphone
- Enable/disable camera
- Responsive UI
- Connection status indicators

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access the application:
- Open your browser and go to `http://localhost:5000`

## Usage

1. Enter a room name on the homepage
2. Share the room name with another user
3. The other user joins using the same room name
4. The video call will automatically establish

## TURN Server Configuration

The application uses the following TURN/STUN servers for remote connectivity:

- STUN: `free.expressturn.com:3478`
- TURN: `free.expressturn.com:3478` (TCP transport)
- Username: `000000002083321464`
- Credential: `jD1BFh+5li2Jy0OQsBqlEwfLB+8=`

Note: This is a free TURN server. For production use, consider using a dedicated TURN server service.

## How It Works

1. **Signaling**: Flask-SocketIO handles signaling between peers
2. **WebRTC**: Browser's WebRTC API handles media streaming
3. **NAT Traversal**: TURN/STUN servers enable connections across different networks
4. **Room System**: Users join rooms to establish peer connections

## Network Requirements

- For local testing: Both users on same network works without TURN
- For remote connections: TURN server is required (already configured)
- Port 5000 must be accessible for Flask server

## Troubleshooting

**Camera/Microphone not working:**
- Ensure browser permissions are granted
- Check if another application is using the camera/mic

**Connection issues:**
- Verify TURN server is accessible
- Check firewall settings
- Ensure both users have stable internet connection

**Audio echo:**
- Use headphones
- Mute microphone when not speaking

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari (may have limitations)

Note: WebRTC requires HTTPS or localhost for camera/microphone access in production.
