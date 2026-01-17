from flask import Flask, render_template, make_response, url_for, redirect # type: ignore
from weasyprint import HTML, CSS # type: ignore
import stripe
import os

app = Flask(__name__)
# Configurar la clave secreta. 
app.config['STRIPE_API_KEY'] = os.environ.get('STRIPE_API_KEY')
stripe.api_key = app.config['STRIPE_API_KEY']


@app.route('/')
def home():
    return '''
    <h1>Bienvenido al Sistema de Fichas</h1>
    <p>Para descargar la ficha, debe realizar el pago de $5.000 CLP.</p>
    <a href="/pagar">
        <button style="padding:10px; background:blue; color:white; border:none; border-radius:5px; cursor:pointer;">
            Pagar y Descargar Ficha
        </button>
    </a>
    '''

id_paciente = 1
@app.route("/ficha/<int:id_paciente>")

def generar_ficha(id_paciente):
    paciente = {
        'id': id_paciente,
        'nombre': 'Juan PEREZ',
        'rut': 210000001,
        'edad': 35,
        'telefono': 56942475843,
        'fecha':'14/2/2012',
        'sexo': 'hombre',
        'altura':'1.98',
        'peso': 90,
        'fecha_nac':'14/01/1983',
        'diagnostico': 'Hipertensión arterial',
        'tratamiento': 'Losartán 50mg cada 12 horas',
        'circulatorio':True,
        'otra_enfermedad': 'otra enfermedad',
        'otra_tiempo':'22/6/2005',
        'cirugias':'cirugias',
        'con_quien_vive': 'con mis papas',
        'sesiones': {
            '1': {'fecha': '2025-05-01', 'lengua': 'Roja', 'pulso': 'Rápido', 'observaciones': 'Sin cambios', 'tecnica_y_puntos': 'Punto A'},
        '2': {'fecha': '2025-05-10', 'lengua': 'Pálida', 'pulso': 'Débil', 'observaciones': 'Mejorando', 'tecnica_y_puntos': 'Punto B'}
        }
    }

    

    html = render_template("ficha3.html", paciente= paciente)
    css_path = os.path.join(app.root_path, 'static', 'style.css')

    pdf = HTML(string=html, base_url=app.root_path).write_pdf(stylesheets=[CSS(filename=css_path)])


    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=ficha_paciente_{id_paciente}.pdf'

    return response

@app.route('/pagar')
def pagar():
    # Creamos una sesión de pago en Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency':'clp', # Moneda chilena
                'product_data': {
                    'name': 'Generación de Ficha Clínica',
                },
                'unit_amount': 5000,
            },
            'quantity':1,
        }],
        mode='payment',
        # A donde redirigir si paga bien:
        success_url=url_for('generar_ficha', id_paciente=1, _external=True),
        # A donde redirigir si cancela:
        cancel_url=url_for('home', _external=True), 
    )

    # Redirigimos al usuario a la pagina de pago de Strie
    return redirect(session.url, code=303)





# @app.route("/formulario")
# def formulario ():
#     return response

if __name__ == "__main__":
    app.run(debug=True)

    