from flask_wtf import FlaskForm
from wtforms import Form, FormField, StringField, SubmitField, FieldList, HiddenField
from wtforms.validators import DataRequired, ValidationError
from app.models import Artist, Song

class ArtistForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    
class SongForm(FlaskForm):
    code = StringField('Code',validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    artists = FieldList(FormField(ArtistForm), min_entries=1)
    submit = SubmitField('Submit')
    
    def validate_code(self, code):
        code = Song.query.filter_by(code=code.data).first()
        if code is not None:
            raise ValidationError('This code is already in the song book.')
            
class PerformanceForm(FlaskForm):
    code = HiddenField()
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')