from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    title = EmailField('Название', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    about = TextAreaField("Немного о товаре", validators=[DataRequired()])
    delivery_date = PasswordField('Время ожидания', validators=[DataRequired()])
    reviews = PasswordField('Отзывы', validators=[DataRequired()])



