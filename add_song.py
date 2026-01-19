import sqlite3
inputs = []
for i in range(5):
    cm = ""
    match i:
        case 0:
            cm = "Titre de la musique: "
        case 1:
            cm = "Nom de l'artiste: "
        case 2:
            cm = "Durée de la musique (en ms): "
        case 3:
            cm = "Index de la musique (n.fichier): "
        case 4:
            cm = "Cover de l'album: "
    inputs.append(input(cm))
database = sqlite3.connect("songs.db")
cursor = database.cursor()
cursor.execute(f"INSERT INTO audios (title,artist,duration,path,cover) VALUES ({inputs[0]},{inputs[1]},{inputs[2]},{inputs[3]},{inputs[4]},)")
number = cursor.fetchone()[0]
database.close()