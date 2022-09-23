import io
from flask import Flask, render_template, request, send_file
from firmador import firmar
from firmador import certificarPdf
import base64
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    return render_template("formulario.html")


@app.route('/procesar',  methods=['POST'])
def procesar():


    
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    # print(json)

    bufferCert = json['bufferCert']
    # print(json)
    linkpdf = json['linkpdf']
    firmas = json['firmas']
    nombre = json['nombre']
    rut = json['rut']
    fecha = json['fecha']
    id = json['id']
    codper = json['codper']

    contraseña = ''
    archivo_pdf_para_enviar_al_cliente = io.BytesIO()
    try:
        datau, datas = firmar(contraseña,bufferCert,linkpdf, firmas, nombre, rut, fecha,id,codper)
        archivo_pdf_para_enviar_al_cliente.write(datau)
        archivo_pdf_para_enviar_al_cliente.write(datas)
        archivo_pdf_para_enviar_al_cliente.seek(0)
        base64send= base64.b64encode(archivo_pdf_para_enviar_al_cliente.read()).decode()
        # return send_file(archivo_pdf_para_enviar_al_cliente, mimetype="application/pdf",
        #                  download_name="firmado" + ".pdf",
        #                  as_attachment=True)
        return base64send
    except ValueError as e:
        return "Error firmando: " + str(e) + " . Se recomienda revisar la contraseña y el certificado"




@app.route('/certificar',  methods=['POST'])
def certificar():

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    # print(json)

    linkpdf = json['linkpdf']
    
    # linkpdf = 'liquidacion.pdf'

    contraseña = ''
    archivo_pdf_para_enviar_al_cliente = io.BytesIO()
    try:
        datau, datas = certificarPdf(contraseña, linkpdf)
        archivo_pdf_para_enviar_al_cliente.write(datau)
        archivo_pdf_para_enviar_al_cliente.write(datas)
        archivo_pdf_para_enviar_al_cliente.seek(0)
        base64send= base64.b64encode(archivo_pdf_para_enviar_al_cliente.read()).decode()
        # return send_file(archivo_pdf_para_enviar_al_cliente, mimetype="application/pdf",
        #                  download_name="firmado" + ".pdf",
        #                  as_attachment=True)
        return base64send
    except ValueError as e:
        return "Error firmando: " + str(e) + " . Se recomienda revisar la contraseña y el certificado"


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=81)
