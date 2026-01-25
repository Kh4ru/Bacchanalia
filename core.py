import sqlite3,os,bcrypt
from flask import Flask,request,send_from_directory,render_template,url_for,session,redirect
from datetime import timedelta
songs_url = os.path.join(os.path.dirname(__file__), 'audios')
covers_url = os.path.join(os.path.dirname(__file__), 'static/covers')

songs = []

class Song:
    def __init__(self,title,author,duration,file,cover):
        self.title = title
        self.author = author
        self.duration = duration
        self.file = file
        self.cover = cover


def list_size():
    database = sqlite3.connect("songs.db")
    cursor = database.cursor()
    cursor.execute("SELECT COUNT(*) audios")
    number = cursor.fetchone()[0]
    database.close()
    return number

def all_songs():
    database = sqlite3.connect("songs.db")
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM audios")
    result = cursor.fetchall()
    database.close()
    return result

def search(text):
    database = sqlite3.connect("songs.db")
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM audios WHERE title LIKE'%{text}%' or artist LIKE '%{text}%'")
    result = cursor.fetchall()
    database.close()
    return result

app = Flask(__name__)
app.secret_key = "itsasecretlol"
app.permanent_session_lifetime = timedelta(days=30)

@app.route("/")
def hello_world():
    if "user_id" not in session:
        return redirect("/login")
    q = request.args.get('q')
    songs = search(q) if q else all_songs()
    length = list_size()
    results = []
    for r in songs:
        cover = f"{r[5]}.jpg"
        file = f"{r[4]}.mp3"
        song = Song(r[1],r[2],r[3],file,cover)
        results.append(song)
    return render_template("index.html",songs=results,q=q,length=length)

@app.route("/login",methods=["GET","POST"])
def login():
    session.permanent = True
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        db = sqlite3.connect("songs.db")
        cur = db.cursor()
        cur.execute("SELECT id, password, name FROM users WHERE userid = ?", (username,))
        row = cur.fetchone()

        if row:
            user_id,password_hash,name = row
            if isinstance(password_hash, str):
                password_hash = password_hash.encode("utf-8")


            if bcrypt.checkpw(password.encode("utf-8"), password_hash):
                session["user_id"] = user_id
                session["name"] = name
                return redirect("/")

        return render_template("login.html", error="Identifiants incorrects")

    return render_template("login.html")



@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        username = request.form["username"].strip()
        password = request.form["password"]
        password = password.encode("utf-8")
        password_hash = bcrypt.hashpw(password,bcrypt.gensalt())
        db = sqlite3.connect("songs.db")
        cur = db.cursor()
        cur.execute(
    "INSERT INTO users (userid, password, name) VALUES (?, ?, ?)",
    (username, password_hash, name))
        db.commit()
        db.close()
        return render_template("account_created.html")
    return render_template("register.html")

@app.route('/logout',methods=["POST"])
def logout():
    session.clear()
    return redirect("/")

@app.route('/play/<filename>')
def get_audio(filename):
    return send_from_directory(songs_url, filename)

@app.route('/image/<filename>')
def get_cover(filename):
    return send_from_directory(covers_url, filename)

