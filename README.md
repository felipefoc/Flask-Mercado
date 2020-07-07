#Flask Mercado
Site em flask feito apenas para estudos.

### O que foi usado ?
- Flask
- SQLAlchemy
- Pillow
- Bootstrap

### E como funciona ?
Primeiro, queria aprender sobre como funciona a integração do _Flask_ com o _HTML_, então comecei usando o

```
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "focky"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```
###### Nesse momento, você define o tempo de cada *session*.
```
app.permanent_session_lifetime = timedelta(minutes=5)
```
###### Aqui você define o banco de dados que vai ser gerado pelo SQLAlchemy
```
db = SQLAlchemy(app) 
```
### Criando as classes
```
class User(db.Model): # Classe USER
    __tablename__ = 'User' # Table
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
```
### e tem mais.. mas vamos falar do uso do Pillow ?
###### O pillow foi usado para tratar as imagens que forem recebidas pelo administrador.. no caso, dando o _resize_

            dir = 'static/upload/' + filename
            image = Image.open(dir)
            newimage = image.resize((250,250))
            newimage.save(dir)
            
# E o bootstrap ?
### Em quase tudo.. mas o projeto ainda está sendo executado, sem tempo definido.. apenas para aprendizado.
Aconselho o uso do [DB Browser for SQLITE](https://sqlitebrowser.org) para vizualização e edição do banco de dados.
# Quais são as próximas etapas ?
- [ ] Resolver NAVBAR
- [ ] Fixar tamanho dos cards na lista de produtos e estilizar a mesma
- [ ] Aprender a usar Blueprints para organizar o projeto
- [ ] Corrigir uso dos flash's
- [ ] E muito mais.

>Felipe Mayer