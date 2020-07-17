from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

artists = db.Table('artists',
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True)
)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f'{self.name}'
        
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    artists = db.relationship('Artist', secondary=artists, lazy='subquery',
        backref=db.backref('songs', lazy=True))
    performances = db.relationship('Performance', backref='song')
    
    def __repr__(self):
        return f'{self.title}'
        
class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'),
        nullable=False)
    completed = db.Column(db.Boolean(), default=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(100))
    
    def __repr__(self):
        return f'{self.username}'
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
@login.user_loader
def load_user(id):
    return User.query.get(int(id))