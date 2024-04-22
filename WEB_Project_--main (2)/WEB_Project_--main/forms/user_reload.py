from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class ReloadForm(FlaskForm):
    name = EmailField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    login = TextAreaField("Почта", validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Обновить данные')


