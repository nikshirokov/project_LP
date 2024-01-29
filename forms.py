from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError




class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
          render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
          render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
         render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
         render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль',validators=[DataRequired(),EqualTo('password')],
         render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!',render_kw={"class": "btn btn-primary"})

    # def validate_username(self, username):
    #     users_count = User.query.filter_by(username=username.data).count()
    #     if users_count > 0:
    #         raise ValidationError('Пользователь с таким именем уже зарегистрирован')