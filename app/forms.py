from flask_wtf import FlaskForm
from wtforms import Form, FormField, StringField, SubmitField, FieldList, HiddenField
from wtforms import PasswordField
from wtforms.validators import DataRequired, ValidationError
from app.models import Artist, Song

class ArtistForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    
class SongForm(FlaskForm):
    id = HiddenField()
    code = StringField('Code',validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    artists = FieldList(FormField(ArtistForm), min_entries=1)
    submit = SubmitField('Submit')
    
    def validate_code(self, code):
        song = Song.query.filter_by(code=code.data).first()
        if not self.id.data:
            if song is not None:
                raise ValidationError('This code is already in the song book.')
        if self.id.data:
            if song is not None and song.id != int(self.id.data):
                raise ValidationError('This code is already in the song book.')
            
class PerformanceForm(FlaskForm):
    code = HiddenField()
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ConfirmDeleteForm(FlaskForm):
    id = HiddenField()
    submit = SubmitField('Delete')