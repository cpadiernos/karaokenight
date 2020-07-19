from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Artist, Song, Performance, User
from app.forms import SongForm, PerformanceForm, LoginForm, ConfirmDeleteForm, SearchForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask import g

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
@login_required
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
    
@app.route('/songs/<id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_song(id):
    song = Song.query.filter_by(id=id).first_or_404()
    form = SongForm(obj=song)
    if form.validate_on_submit():
        song.title = form.title.data
        song.code = form.code.data
        song.artists[:] = []
        names = [artist['name']for artist in form.artists.data]
        for name in names:
            artist = Artist.query.filter_by(name=name).first()
            if artist:
                song.artists.append(artist)
            else:
                artist = Artist(name=name)
                db.session.add(artist)
                song.artists.append(artist)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('song_form.html', title='Edit Song', form=form)
    
@app.route('/songs/<id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_song(id):
    song = Song.query.filter_by(id=id).first_or_404()
    form = ConfirmDeleteForm(obj=song)
    if form.validate_on_submit():
        db.session.delete(song)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('confirm_delete.html', title='Delete Song', form=form, song=song)

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
    
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
    
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.before_request
def before_request():
    g.search_form = SearchForm()
    
@app.route('/search/')
def search():
    songs, total = Song.search(g.search_form.q.data, 1, 100) # page 1, 100 records per page
    if g.search_form.q.data == "":
        songs = Song.query.all()
        return render_template('song_table.html', songs=songs)
    if total > 0: 
        return render_template('song_table.html', songs=songs)
    else:
        return render_template('song_table.html', songs=False)