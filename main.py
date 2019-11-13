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

# conectar Base de Datos
bd = Base_datos('localhost', 'root', 'root', 'registro')


""" INICIO """
@app.route('/', methods=['GET','POST'])
def inicio():
    if request.method == 'POST':
        session.clear()
        bd.cerrar()

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
        leer_email = bd.query(
            f'SELECT email FROM usuario WHERE email="{email}"'
        )
        if leer_email != ():
            
            leer_email_password = bd.query(
            f'SELECT email,password,nombre FROM usuario WHERE email="{email}"')
            
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
        leer_email = bd.query(
            f'SELECT email FROM usuario WHERE email="{email}"'
        )
        if leer_email != ():
            return render_template('registro.html', usuario_no=True)

        # registrar en la base de datos
        leer_email = bd.query(
            f'INSERT INTO usuario VALUES(null,"{nombre}","{email}","{password}",1)'
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
        return redirect(url_for('/'))

    frase = f'session: {email} / {password}'


    return render_template('entrar.html', frase=frase, nombre=nombre)



if __name__ == "__main__":
    app.run(debug=True)