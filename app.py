from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import timedelta
import os
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "focky"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)
app_root = os.path.dirname(os.path.abspath(__file__))

db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static\\upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25))
    username = db.Column(db.String(25))
    senha = db.Column(db.String(25))
    nome = db.Column(db.String(15))
    sobrenome = db.Column(db.String(15))
    cep = db.Column(db.String(9))
    numero = db.Column(db.String(5))
    comp = db.Column(db.String(10))
    endereco = db.Column(db.String(25))
    admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, email, username, senha, nome, sobrenome, cep, numero, comp, endereco, admin):
        self.email = email
        self.username = username
        self.senha = senha
        self.nome = nome
        self.sobrenome = sobrenome
        self.cep = cep
        self.numero = numero
        self.comp = comp
        self.endereco = endereco
        self.admin = admin


class Produtos(db.Model):
    __tablename__ = 'Produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25))
    setor = db.Column(db.String(25))
    valor = db.Column(db.Float(10))
    qntd = db.Column(db.Integer)
    nome_img = db.Column(db.String(25))

    def __init__(self, nome, setor, valor, qntd, nome_img):
        self.nome = nome
        self.setor = setor
        self.valor = valor
        self.qntd = qntd
        self.nome_img = nome_img


x = User.query.all()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    flash('Logado como administrador {}'.format(session['logado']))
    if request.method == 'POST':
        produtonome = request.form['produtonome']
        setor = request.form['setor']
        valor = request.form['valor']
        file = request.files['imgproduto']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('cadastrodeprodutos.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            dir = 'static/upload/' + filename
            image = Image.open(dir)
            newimage = image.resize((250,250))
            newimage.save(dir)
            add = Produtos(produtonome, setor, valor, 1, filename)
            db.session.add(add)
            db.session.commit()
        flash('Saved')
        return redirect(url_for('cadastro'))
    return render_template('cadastrodeprodutos.html')


@app.route('/', methods=["GET", "POST"])
def login():
    session['logado'] = False
    if request.method == "POST":
        email = request.form['emaillogin']
        senha = request.form['passwordlogin']
        emailfound = User.query.filter_by(email=email).first()
        senhafound = User.query.filter_by(senha=senha).first()
        try:
            if emailfound.id == senhafound.id and emailfound.admin == True:
                session['logado'] = emailfound.nome
                return redirect(url_for('cadastro'))
            if emailfound.id == senhafound.id and emailfound.admin == False:
                session['logado'] = emailfound.nome
                return redirect(url_for('produtos'))
        except AttributeError:
            flash('Dados inválidos, tente novamente.')
            return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/registrar', methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        try:
            email = request.form['emailuser']
            senha = request.form['senha']
            endereco = request.form['endereco']
            numero = request.form['numero']
            comp = request.form['comp']
            nome = request.form['nome']
            username = request.form['username']
            sobrenome = request.form['sobrenome']
            cep = request.form['cep']
            admin = 0
            add = User(email, username, senha, nome, sobrenome, cep, numero, comp, endereco, admin)
            db.session.add(add)
            db.session.commit()
        except exc.IntegrityError:
            flash('Email já cadastrado, tente novamente.')
            return redirect(request.url)
        flash('Cadastro efetuado com sucesso')
    return render_template('register.html')


@app.route('/produtos')
def produtos():
    produtos = Produtos.query.all()
    return render_template('produtos.html', produtos=produtos)


@app.route('/logout')
def logout():
    session.pop('logado', None)
    session.pop('newuser', None)
    return redirect(url_for('login'))


@app.route('/listadeprodutos')
def listadeprodutos():
    produtos = Produtos.query.all()
    return render_template('listaprodutos.html', produtos=produtos)


@app.route('/delete<numeroid>', methods=['GET'])
def delete(numeroid):
    Produtos.query.filter_by(id=numeroid).delete()
    db.session.commit()
    flash('Deletado com sucesso')
    return redirect('listadeprodutos.html')




if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
