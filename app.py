from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'Nilo2020+'  # Cambia esta clave por una clave segura

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pedromesaglio05@gmail.com'  # Cambia esto a tu correo
app.config['MAIL_PASSWORD'] = 'Nilo2020+'        # Cambia esto a tu contraseña de correo

mail = Mail(app)

@app.before_request
def log_visit():
    visitor_ip = request.remote_addr  # Obtener la IP del visitante
    access_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_agent = request.headers.get('User-Agent')
    
    # Registrar la IP, la fecha y el navegador en un archivo
    with open("log.txt", "a") as log_file:
        log_file.write(f"IP: {visitor_ip}, Fecha: {access_time}, Navegador: {user_agent}\n")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    # Puedes mantener tu código actual para mostrar proyectos
    return render_template('projects.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Crear y enviar el correo
        msg = Message(subject=f"Mensaje de {name}",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']],
                      body=f"Nombre: {name}\nCorreo: {email}\n\nMensaje:\n{message}")
        mail.send(msg)
        
        flash("¡Mensaje enviado correctamente!")
        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)