import sqlite3,os
from flask import Flask,request,send_from_directory,render_template,url_for
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

@app.route("/")
def hello_world():
    q = request.args.get('q')
    songs = search(q) if q else all_songs()
    length = list_size()
    results = []
    for r in songs:
        cover = f"{r[5]}.jpg"
        file = f"{r[4]}.mp3"
        song = Song(r[1],r[2],r[3],file,cover)
        results.append(song)
    return render_template("web_client.html",songs=results,q=q,length=length)

@app.route('/play/<filename>')
def get_audio(filename):
    return send_from_directory(songs_url, filename)

@app.route('/image/<filename>')
def get_cover(filename):
    return send_from_directory(covers_url, filename)

