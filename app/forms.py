from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired

class inputForm(FlaskForm):
    """ sql form format:
        variable = fieldtype('variable name', [validators = [validator type], message = "error message"])
    """
    
    # input 1 upload seqeunce
    sequenceFile = FileField(
        'Sequence File', validators = [DataRequired(), FileAllowed(['csv', 'txt'], 'csv and txt files only')])
    # input -> name
    name = StringField(
        'Name*',
        [DataRequired()]
    )
    # input -> email
    email = StringField(
        'Email*',
        [
            DataRequired(),
            Email(message = ('Not a valid email address.'))
            
        ]
    )
    submit = SubmitField('Submit')

    # def validate(self):
    #     if not super(inputForm, self).validate():
    #         return False
    #     if not self.textSequence.data and not self.sequenceFile.data:
    #         message = "at least one of the field must be filled out"
    #         self.textSequence.append(message)
    #         self.sequenceFile.append(message)
    #         return False
    #     return True