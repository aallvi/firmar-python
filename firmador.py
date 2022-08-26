# *-* coding: utf-8 *-*
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
import fitz
from endesive.pdf import cms
import json
import base64


import logging
def firmar(contraseña, certificado, pdf):
    
    

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
         "signaturebox": (0, 0, 590, 155),
        "signature": "Aquí va la firma 2",
        # "signature_img": "signature_test.png",
        "contact": "hola@ejemplo.com",
        "location": "Ubicación",
        "signingdate": date,
        "reason": "Razón",
        "password": contraseña,
    }
    # with open("cert.p12", "rb") as fp:
    p12 = pkcs12.load_key_and_certificates(
        certificado.read(), contraseña.encode("ascii"), backends.default_backend()
    )

    #datau = open(fname, "rb").read()

    
    datau = pdf.read()

    print(type(certificado.read()))

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
