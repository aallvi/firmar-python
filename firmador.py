# *-* coding: utf-8 *-*
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
# import fitz
from endesive.pdf import cms
import json
import base64
from urllib.request import urlopen
import io
import os
import qrcode
import logging
from PyPDF2 import PdfFileReader

def certificarPdf(contraseña, linkpdf):
    
    link = linkpdf
    url = f"https://websalsign.s3.amazonaws.com/{link}"

    print(url)

    urlp12 = 'https://websalsign.s3.amazonaws.com/2676/websal.p12'

    with urlopen(url) as file:
      content = file.read()
        
    # print(content)

    with urlopen(urlp12) as file:
      contentp12 = file.read()
    # print(content)


    print('-------------------------------------------')


    date = datetime.datetime.utcnow() 
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "sigbutton": True,
        "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        # "signaturebox": (470, 840, 570, 640),
        #  "signaturebox": (0, 0, 590, 155),
        # "signature": "Aquí va la firma 22323",
        # "signature_img": "signature_test.png",
        "contact": "contacto@websal.com",
        "location": "Ubicación",
        "signingdate": date,
        "reason": "Razón",
        "password": contraseña,
    }
    # with open("cert.p12", "rb") as fp:
    p12 = pkcs12.load_key_and_certificates(
        contentp12, contraseña.encode("ascii"), backends.default_backend()
    )

    #datau = open(fname, "rb").read()

    
    datau = content
    
    # print(datau)

    # print(type(certificado.read()))

    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")

    # print(type(datas))

    base64_encoded_data = base64.b64encode(datas)
    base64_message = base64_encoded_data.decode('utf-8')
    
 
 

    return datau, datas
    """
    fname = "test.pdf"
    with open(fname, "wb") as fp:
        fp.write(datau)
        fp.write(datas)
    """

def firmar(contraseña, bufferCert, linkpdf, firmas, nombre, rut, fecha,id,codper):

    
    link = linkpdf
    url = f"https://websalsign.s3.amazonaws.com/{link}"

    # print(url)

    with urlopen(url) as file:
      content = file.read()
    
     # Conteo de paginas
    
    memory_file = io.BytesIO(content)
    pdf_file = PdfFileReader(memory_file)
    
    totalpages = pdf_file.numPages

    # qr

    img = qrcode.make(f'http://localhost:3001/#/verpdf/{id}/{codper}')

    qrName = f'qr{id}.png'
    
    with open(qrName, 'wb') as qr:
     img.save(qr)
    # print(type(img))

   
    # print(content)


    print('-------------------------------------------')

    # leemos el buffer del certificado y los transformamos a bytes
    x = bufferCert['data']
   


    byte_arrayCert = bytearray(x)
    # print(byte_arrayCert)

    date = datetime.datetime.utcnow() 
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")


    if firmas == 0 :
       signatureBox = (380, 10, 480, 100)
    else:
       signatureBox = (500, 10, 600, 100)

    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": totalpages-1,
        "text":{
            "fontsize":7, "textalign":'center', "linespacing":1.2
        },
        "sigbutton": True,
        "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        # "signform": True,
                    #  distancia de la izq, distancia de abajo, distancia derecha, distancia hacia arriba
        "signaturebox": signatureBox,
        "signature_manual": [
            #                R     G     B
            ['fill_colour', 0, 0, 0.95],

            #            *[bounding box]
            ['rect_fill', 0, 0, 0, 0],

            #                  R    G    B
            ['stroke_colour', 255, 255, 255],

            #        inset
            ['border', 0.1],

            #          key  *[bounding box]  distort centred
            ['image', 'sig0', 20, 100, 80, 20,  False, True],

            #         font     fs 
            ['font', 'default', 7],
            #               R  G  B
            ['fill_colour', 0, 0, 0],

            #            text
            ['text_box', f'Firma Digital - {nombre} {rut} {fecha}',
                # font  *[bounding box], fs, wrap, align, baseline
         # distancia de la izquierda, distancia del suelo , ancho
                'default', 1, 28, 100, 2, 7, True, 'center', 'top'],
            ],
        #   key: name used in image directives
        # value: PIL Image object or path to image file
        "manual_images": {'sig0': qrName},
        #   key: name used in font directives
        # value: path to TTF Font file
        "manual_fonts": {},
        # "signature_appearance": {
        #     'background': [0.75, 0.8, 0.95],
        #     'icon': img,
        #     'outline': [0.2, 0.3, 0.5],
        #     'border': 2,
        #     'labels': True,
        #     'display': 'CN,DN,date,contact,reason,location'.split(','),
        #     },
        # "signature": "Firma Digital - Alvaro Agustin Leiva Gil 196056920 el 15/ag/2022 a las 19:48",
        # "signature_img": 'qr.png',
        "contact": "hola@ejemplo.com",
        "location": "Ubicación",
        "signingdate": date,
        "reason": "Razón",
        "password": contraseña,
    }



    # with open("cert.p12", "rb") as fp:
    p12 = pkcs12.load_key_and_certificates(
        byte_arrayCert, contraseña.encode("ascii"), backends.default_backend()
    )

    #datau = open(fname, "rb").read()

    
    datau = content
    



    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")

    # print(type(datas))

   
    
 
    os.remove(qrName)

    return datau, datas
    """
    fname = "test.pdf"
    with open(fname, "wb") as fp:
        fp.write(datau)
        fp.write(datas)
    """
