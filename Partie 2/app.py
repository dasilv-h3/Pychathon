from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from utils.utils import room_code_generator

app = Flask(__name__)
app.config["SECRET_KEY"] = "grqdsgq"
socketio = SocketIO(app)

# rooms = {code:{members:int, messages:list}}
rooms = {}

# View principal Créer et rejoindre un salon
@app.route('/',methods=["POST", "GET"])
def index():
    session.clear()
    context = {}
    if request.method == "POST":
        username = request.form.get("username")
        code = request.form.get("code")
        join = request.form.get("join")
        create = request.form.get("create")
        
        if not username:
            return render_template('home.html', error="Entrez un pseudo", code=code)
        
        if join and not code:
            return render_template('home.html', error="Entrez un code", code=code, name=username)
        
        if create:
            code = room_code_generator(4, rooms)
            rooms[code] = {"members": 0, "messages": []}
        elif code not in rooms:
            print("not code in rooms")
            return render_template('home.html', error="Le salon n'existe pas !", code=code, name=username)

        session["code"] = code
        session["username"] = username
        return redirect(url_for("room"))
    
    return render_template('home.html', context=context)

# View du salon
@app.route("/room")
def room():
    print(session)
    code = session.get("code")
    print("ROOM:", code)
    if code is None or session.get("username") is None or code not in rooms:
        return redirect(url_for("index"))
    return render_template("room.html", code=code)

@socketio.on("message")
def message(data):
    room = session.get("code")
    if room not in rooms:
        return 
    
    content = {
        "username": session.get("username"),
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(rooms[room]["messages"])
    print(f"{session.get('username')} dit: {data['data']}")

# Connexion au salon
@socketio.on("connect")
def connect():
    room = session.get("code")
    username = session.get("username")
    if not room or not username:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"username": username, "message": "a rejoint le salon"}, to=room)
    rooms[room]["members"] += 1
    print(f"{username} a rejoint le salon {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("code")
    username = session.get("username")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"username": username, "message": "a quitté le salon"}, to=room)
    print(f"{username} a quitté le salon {room}")
    
if __name__ == '__main__':
    socketio.run(app, debug=True)