from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models import Artist, Song
from app.forms import SongForm

@app.route('/')
def index():
    songs = Song.query.all()
    return render_template('index.html',
        title='Song list',
        songs=songs)
        
@app.route('/songs/new/', methods=['GET', 'POST'])
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        song = Song(code=form.code.data, title=form.title.data)
        artist_list = form.artists.data.split(',')
        artists = [artist.strip() for artist in artist_list]
        for name in artists:
            artist = Artist.query.filter_by(name=name).first()
            if artist:
                song.artists.append(artist)
            else:
                artist = Artist(name=name)
                db.session.add(artist)
                song.artists.append(artist)
        db.session.add(song)
        db.session.commit()
        flash('"{}" by {} - added.'.format(song.title, ', '.join([artist.name for artist in song.artists])))
        return redirect(url_for('index'))
    return render_template('song_form.html', title='Add Song', form=form)