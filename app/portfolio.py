from flask import (
    Blueprint,render_template,request,redirect,url_for,current_app
)
import sendgrid
from sendgrid.helpers.mail import *
from werkzeug.wrappers import response

bp = Blueprint('portfolio', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('portfolio/index.html')
    
@bp.route('/mail',methods=['GET','POST'])
def mail():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if request.method == 'POST':
        send_email(name, email, message)
        return render_template('portfolio/sent_mail.html')
    
    return redirect(url_for('portfolio.index'))

def send_email(name, email, message):
    mi_email = 'apomte_1@hotmail.com'
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])

    from_email =Email(mi_email)# quien esta enviando el correo
    to_email = To(mi_email, substitutions={
        "-name-": name,
        "-email-": email,
        "-message-": message,
    })# a quien se lo vamos a enviar
    #substitutions me va a reeplazar las variables de mas abajo, lo pasamos como un diccionario

    #para no recibir un contenido plano creamos uno html
    # las -variables- son los string que vamos a reeplazar 
    html_content = """
        <p> Hola Jefferson , tienes un nuevo contacto desde la web:</p>
        <p>Nombre: -name-</p>
        <p>Correo: -email-</p>
        <p>Mensaje: -message-</p>
    """
    mail = Mail(mi_email,to_email , 'Nuevo contacto desde la web', html_content=html_content)#de donde viene ,a donde va , un mensaje y el html que creamos se lo devolvemos
    response = sg.client.mail.send.post(request_body=mail.get())