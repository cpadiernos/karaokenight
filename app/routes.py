from flask import render_template
from app import app
from app.models import Song

@app.route('/')
def index():
    songs = Song.query.all()
    return render_template('index.html',
        title='Song list',
        songs=songs)