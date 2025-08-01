from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import os

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = os.urandom(24)

# Session configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=["GET", "POST"])
def index():
    if 'notes' not in session:
        session['notes'] = []

    if request.method == "POST":
        note = request.form.get("note")
        if note:
            session['notes'].append(note)
            session.modified = True
        return redirect(url_for('index'))

    indexed_notes = list(enumerate(session['notes']))
    return render_template("home.html", notes=indexed_notes)

@app.route('/edit/<int:note_index>', methods=["GET", "POST"])
def edit_note(note_index):
    if 'notes' not in session or note_index >= len(session['notes']):
        return redirect(url_for('index'))

    if request.method == "POST":
        new_note = request.form.get("new_note")
        if new_note:
            session['notes'][note_index] = new_note
            session.modified = True
        return redirect(url_for('index'))

    return render_template("edit.html", note_index=note_index)

@app.route('/delete/<int:note_index>', methods=["POST"])
def delete_note(note_index):
    if 'notes' in session and note_index < len(session['notes']):
        del session['notes'][note_index]
        session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
