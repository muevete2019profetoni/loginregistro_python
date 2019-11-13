"""
    ----------------
    LOGIN & REGISTRO
    ----------------
    v.1.0 login y registro de app en Python
    v.0.2 SQL de usuarios
"""


# inicializar librerias
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect,url_for
from flask import session

from lib.conexionMySQL import Base_datos

app = Flask(__name__)
app.secret_key = 'todoSuperSecreto'


""" INICIO """
@app.route('/', methods=['GET','POST'])
def inicio():
    if request.method == 'POST':
        session.clear()

    if 'email' in session:
        return redirect(url_for('entrar'))

    return render_template('inicio.html')


""" LOGIN """
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('correo')
        password = request.form.get('contrasenya')
        # base de datos - validar
        bd = Base_datos('localhost', 'root', 'root', 'registro')
        leer_email = bd.query(
            f'SELECT email FROM registrado WHERE email="{email}"'
        )
        if leer_email != ():
            bd_total = Base_datos('localhost', 'root', 'root', 'registro')
            leer_email_password = bd_total.query(
                f'SELECT email,password,nombre FROM registrado WHERE email="{email}"'
            )
            if leer_email_password[0][0] == email and leer_email_password[0][1] == password:
                # iniciar session
                session['nombre'] = leer_email_password[0][2] 
                session['email'] = email 
                session['password'] = password

                return redirect(url_for('entrar'))


        return render_template('login.html', usuario_no=True)     

    return render_template('login.html')





""" REGISTRO """
@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('correo')
        password = request.form.get('contrasenya')
        # base de datos - validar
        bd = Base_datos('localhost', 'root', 'root', 'registro')
        leer_email = bd.query(
            f'SELECT email FROM registrado WHERE email="{email}"'
        )
        if leer_email != ():
            return render_template('registro.html', usuario_no=True)

        # registrar en la base de datos
        bd = Base_datos('localhost', 'root', 'root', 'registro')
        leer_email = bd.query(
            f'INSERT INTO registrado VALUES(null,"{nombre}","{email}","{password}",1)'
        )
        return redirect(url_for('login'))


    return render_template('registro.html')





""" ENTRAR """
@app.route('/entrar', methods=['GET','POST'])
def entrar():
    if 'email' in session:
        nombre = session['nombre']
        email = session['email']
        password = session['password']
    else:
        email = ''

    frase = f'session: {email} / {password}'


    return render_template('entrar.html', frase=frase, nombre=nombre)



if __name__ == "__main__":
    app.run(debug=True)