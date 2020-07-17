from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models import Artist, Song, Performance
from app.forms import SongForm, PerformanceForm

@app.route('/', methods=['GET', 'POST'])
def index():
    songs = Song.query.all()
    form = PerformanceForm()
    if form.validate_on_submit():
        song = Song.query.filter_by(code=form.code.data).first()
        performance = Performance(name=form.name.data, song_id=song.id)
        db.session.add(performance)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html',
        title='Song list',
        songs=songs, form=form)
        
@app.route('/songs/new/', methods=['GET', 'POST'])
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        song = Song(code=form.code.data, title=form.title.data)
        names = [artist['name']for artist in form.artists.data]
        for name in names:
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
    
@app.route('/performances/')
def view_performances():
    performances = Performance.query.filter_by(completed=False).all()
    return render_template('performance_base.html', performances=performances)
    
@app.route('/performances/<id>/delete/', methods=['POST'])
def delete_performance(id):
    performance = Performance.query.filter_by(id=id).first()
    db.session.delete(performance)
    db.session.commit()
    return redirect(url_for('view_performances'))
    
@app.route('/performances/<id>/complete/', methods=['POST'])
def mark_performance_completed(id):
    performance = Performance.query.filter_by(id=id).first()
    performance.completed = True
    db.session.commit()
    performances = Performance.query.filter_by(completed=False).all()
    return render_template('performance_table.html', performances=performances)
    
@app.route('/performances/<id>/uncomplete/', methods=['POST'])
def mark_performance_uncompleted(id):
    performance = Performance.query.filter_by(id=id).first()
    performance.completed = False
    db.session.commit()
    performances = Performance.query.filter_by(completed=False).all()
    return render_template('performance_table.html', performances=performances)