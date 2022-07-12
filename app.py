from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_conntection():
    try:
        conn = sqlite3.connect("notes.sqlite")
    except sqlite3.error as e:
        print(e)
        return None
    return conn

@app.route("/notes", methods=["GET", "POST"])
def all_notes():
    conn = get_conntection()
    cursor = conn.cursor()

    # shows full list of all notes
    if request.method == "GET":
        notes = cursor.execute("SELECT * FROM notes").fetchall()
        if len(notes) != 0:
            return jsonify(notes)
        else:
            return "No notes found"

    # adds new note to the database
    if request.method == "POST":
        content = request.form["content"]

        sql = """INSERT INTO notes (content)
                 VALUES (?)"""

        cursor.execute(sql, (content,))
        conn.commit()
        return "New note added successfully"

@app.route("/note/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_note(id):
    conn = get_conntection()
    cursor = conn.cursor()

    # displays the note to the user
    if request.method == "GET":
        note = cursor.execute("SELECT * FROM notes WHERE id=?", (id,)).fetchall()
        if len(note) != 0:
            return jsonify(note)
        else:
            return "No note found"

    # updates the note with new content
    if request.method == "PUT":
        content = request.form["content"]

        sql = """UPDATE notes
                  SET content = ?
                  WHERE id = ?"""

        cursor.execute(sql, (content, id))
        conn.commit()

        return "Note updated"

    # deletes the note with the given id
    if request.method == "DELETE":
        sql = "DELETE FROM notes WHERE id = ?"
        cursor.execute(sql, (id,))
        conn.commit()

        return "Note deleted"

if __name__ == "__main__":
    app.run(debug=True)
