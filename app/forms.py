from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Artist, Song

class SongForm(FlaskForm):
    code = StringField('Code',validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    artists = StringField('Artist(s)', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def validate_code(self, code):
        code = Song.query.filter_by(code=code.data).first()
        if code is not None:
            raise ValidationError('This code is already in the song book.')