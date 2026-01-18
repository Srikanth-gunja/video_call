import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "video-call-secret-key")

# Use eventlet for production; allow CORS for all origins
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/call/<room_id>")
def call(room_id):
    return render_template("call.html", room_id=room_id)


@socketio.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)
    emit("user_joined", {"user": request.sid}, room=room, skip_sid=request.sid)


@socketio.on("leave")
def on_leave(data):
    room = data["room"]
    leave_room(room)
    emit("user_left", {"user": request.sid}, room=room)


@socketio.on("offer")
def on_offer(data):
    emit(
        "offer",
        {"offer": data["offer"], "user": request.sid},
        room=data["room"],
        skip_sid=request.sid,
    )


@socketio.on("answer")
def on_answer(data):
    emit(
        "answer",
        {"answer": data["answer"], "user": request.sid},
        room=data["room"],
        skip_sid=request.sid,
    )


@socketio.on("ice_candidate")
def on_ice_candidate(data):
    emit(
        "ice_candidate",
        {"candidate": data["candidate"], "user": request.sid},
        room=data["room"],
        skip_sid=request.sid,
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
        allow_unsafe_werkzeug=True,  # Required for Render deployment
    )
