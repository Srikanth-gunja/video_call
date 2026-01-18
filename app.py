import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "video-call-secret-key")

# Track users in rooms
rooms = {}

# Use simple-websocket for proper async WebSocket handling
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode="threading",
    logger=True,
    engineio_logger=True
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/call/<room_id>")
def call(room_id):
    return render_template("call.html", room_id=room_id)


@socketio.on("join")
def on_join(data):
    room = data["room"]
    sid = request.sid
    
    join_room(room)
    
    # Track users in room
    if room not in rooms:
        rooms[room] = []
    rooms[room].append(sid)
    
    print(f"User {sid} joined room {room}. Total users: {len(rooms[room])}")
    
    # Notify others in the room
    emit("user_joined", {"user": sid}, room=room, skip_sid=sid)


@socketio.on("leave")
def on_leave(data):
    room = data["room"]
    sid = request.sid
    
    leave_room(room)
    
    # Remove from room tracking
    if room in rooms and sid in rooms[room]:
        rooms[room].remove(sid)
        if not rooms[room]:
            del rooms[room]
    
    print(f"User {sid} left room {room}")
    emit("user_left", {"user": sid}, room=room)


@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    print(f"User {sid} disconnected")
    
    # Remove from all rooms
    for room in list(rooms.keys()):
        if sid in rooms[room]:
            rooms[room].remove(sid)
            emit("user_left", {"user": sid}, room=room)
            if not rooms[room]:
                del rooms[room]


@socketio.on("offer")
def on_offer(data):
    sid = request.sid
    print(f"Relaying offer from {sid} to room {data['room']}")
    emit(
        "offer",
        {"offer": data["offer"], "user": sid},
        room=data["room"],
        skip_sid=sid,
    )


@socketio.on("answer")
def on_answer(data):
    sid = request.sid
    print(f"Relaying answer from {sid} to room {data['room']}")
    emit(
        "answer",
        {"answer": data["answer"], "user": sid},
        room=data["room"],
        skip_sid=sid,
    )


@socketio.on("ice_candidate")
def on_ice_candidate(data):
    sid = request.sid
    print(f"Relaying ICE candidate from {sid} to room {data['room']}")
    emit(
        "ice_candidate",
        {"candidate": data["candidate"], "user": sid},
        room=data["room"],
        skip_sid=sid,
    )


if __name__ == "__main__":
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 5000))
    # Disable debug in production
    debug = os.environ.get("FLASK_ENV") != "production"
    
    socketio.run(
        app, 
        host="0.0.0.0", 
        port=port, 
        debug=debug,
        allow_unsafe_werkzeug=True  # Required for Render deployment
    )
