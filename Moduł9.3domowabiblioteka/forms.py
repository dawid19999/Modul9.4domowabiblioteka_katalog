from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class BookForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired(), Length(min=1, max=100)])
    author = StringField('Autor', validators=[DataRequired(), Length(min=1, max=100)])
    year = IntegerField('Rok wydania', validators=[DataRequired(), NumberRange(min=0, max=2100)])
    description = TextAreaField('Opis', validators=[Length(max=500)])
