from flask import Flask, render_template, url_for, redirect, request, abort
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms.user_activarion import LoginForm
from forms.user_reload import ReloadForm
from data import db_session
from data.product import Product
from data.users import User
from forms.users import RegisterForm
from data.kategory import Kategory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    slides = db_sess.query(Product).all()
    return render_template("main.html", title='Главная страница', products=slides)


@app.route("/tovar/<int:id>")
@login_required
def product(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id).first()
    return render_template("tovar.html", title='Просмотр товара', tovar=product, user=current_user)


@app.route("/korzina")
@login_required
def korzina():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    tovar = []
    id_tovar = []
    kol = []
    if user.prods:
        for item in str(user.prods).split():
            if int(item) not in id_tovar:
                tovar.append(db_sess.query(Product).filter(Product.id == item).first())
                id_tovar.append(tovar[-1].id)
                kol.append(1)
            else:
                kol[id_tovar.index(int(item))] += 1
    return render_template("korzina.html", title='Корзина', tovar=tovar, kol=kol)


@app.route("/addkorzina/<int:id>")
@login_required
def addkorzina(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user.prods:
        user.prods = str(user.prods) + f' {str(id)}'
    else:
        user.prods = str(id)
    db_sess.commit()
    return redirect('/korzina')


@app.route("/clear")
@login_required
def clear():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.prods = ''
    db_sess.commit()
    return redirect('/korzina')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('lk.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            login=form.login.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('lk.html', title='Регистрация', form=form)


@app.route("/lk", methods=['GET', 'POST'])
@login_required
def lk():
    form = ReloadForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
            form.login.data = user.login
            form.password.data = user.password
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            user.name = form.name.data
            user.surname = form.surname.data
            user.login = form.login.data
            form.password.data = user.password
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('lk.html', title='Личный кабинет', form=form)


@app.route("/kateg")
def kategori():
    db_sess = db_session.create_session()
    kateg = db_sess.query(Kategory).all()
    return render_template('kategori.html', title='Категории товаров', kateg=kateg)


@app.route("/kategory/<int:kat>")
def kategori_list(kat):
    db_sess = db_session.create_session()
    products = db_sess.query(Product).filter(Product.kategory_id == kat).all()
    kateg = db_sess.query(Kategory).filter(Kategory.id == kat).first().title
    return render_template('main.html', title=f'Категория {kateg}', products=products)


@app.route("/zakaz")
@login_required
def zakaz():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user.pokupka:
        user.pokupka = user.pokupka + ' ' + user.prods
    else:
        user.pokupka = user.prods
    user.prods = ''
    db_sess.commit()
    return index()


def main():
    db_session.global_init("db/online_shop.db")
    app.run()


if __name__ == '__main__':
    main()
