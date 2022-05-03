from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class SignupForm(FlaskForm):
    name = StringField(
        'Nombre', validators=[DataRequired(), Length(max=24)]
    )
    surname_1 = StringField(
        'Apellido Paterno', validators=[DataRequired(), Length(max=20)]
    )
    surname_2 = StringField(
        'Apellido Materno', validators=[DataRequired(), Length(max=20)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
    )
    phone = StringField(
        'Teléfono', validators=[DataRequired(), Length(max=9)]
    )
    submit = SubmitField('Registrar')


class OtpFileForm(FlaskForm):
    upload = FileField(
        'Document OTP', 
        validators=[
            FileRequired(),
            FileAllowed(["pdf"], "Solo se aceptan archivos PDF")
        ]
    )
    submit = SubmitField('Enviar')


class OtpForm(FlaskForm):
    otp = StringField(
        'Código OTP', validators=[DataRequired(), Length(max=6)]
    )
    submit = SubmitField('Registrar')
