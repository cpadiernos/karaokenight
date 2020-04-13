from app import db

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
    
    def __repr__(self):
        return f'{self.title}'
