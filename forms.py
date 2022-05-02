from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=24)])
    last_name = StringField('Apellidos', validators=[DataRequired(), Length(max=74)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(max=9)])
    submit = SubmitField('Registrar')
