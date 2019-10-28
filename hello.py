from flask import Flask,g,session,request,redirect,url_for,make_response
import click,os

app = Flask(__name__)
app.secret_key= os.getenv('SECRET_KEY', '888666')
print(app.secret_key)

@app.before_request
def get_name():
    g.name = request.args.get('name')

@app.route('/')
def index():
    return '%s,你好' % g.name

@app.cli.command()
def dayin():
    click.echo('随便打印啥东西')

@app.route('/<name>')
def aa(name):
    res = make_response(redirect(url_for('index')))
    res.set_cookie('name',name)
    return res

@app.route('/login')
def login():
    session['logged_in'] = True # 写入session
    return redirect(url_for('index'))