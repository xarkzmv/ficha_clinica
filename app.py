from flask import Flask, render_template, make_response, url_for # type: ignore
from weasyprint import HTML, CSS # type: ignore
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Servidor Flask Funcionando!'

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

# @app.route("/formulario")
# def formulario ():
#     return response

if __name__ == "__main__":
    app.run(debug=True)

    