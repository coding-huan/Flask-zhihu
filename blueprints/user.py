from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from exts import mail, db
from flask_mail import Message
from models import EmailCapatchaModel, UserModel
import random
from datetime import datetime
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form);
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect('/')
            else:
                flash('邮箱和密码不匹配')
                return redirect(url_for('user.login'))
        else:
            flash('邮箱或密码格式错误')
            return redirect(url_for('user.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    form = RegisterForm(request.form)
    if form.validate():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        hash_pwd = generate_password_hash(password)
        user = UserModel(username=username, password=hash_pwd, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))
    else:
        return redirect(url_for('user.register'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))


# memcached/redis/数据库中
@bp.route('/captcha', methods=['POST'])
def get_captcha():
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    captcha = ''.join(random.sample(digits, 6))
    email = request.form.get('email')
    if email:
        message = Message(
            subject='知乎验证码',
            recipients=[email],
            body='您的验证码是' + captcha
        )
        mail.send(message)
        captcha_model = EmailCapatchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCapatchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()

        # code: 200，成功的请求
        return jsonify({'code': 200})
    else:
        # code: 400 客户端错误
        return jsonify({'code': 400, 'message': '请先传递邮箱'})
