# additional dependencies:
#    libcml2-dev libxmlsec1-dev libxmlsec1-openssl

# TLS cipher hack (use if necessary)
# import urllib3
# urllib3.util.ssl_.DEFAULT_CIPHERS = 'HIGH:!DH:!aNULL'

import xmlsec
from zeep import Client
from zeep.wsse import BinarySignature, KeysInfo

# specify key paths
# assumptions:
#    - ebudownictwo.key is a private key of a client
#    - ebudownictwo.cer is a x509 certificate issued by PZ admin
#    - pz.cer is a PZ certificate used to verify response messages
#    - password.txt contains password to the ebudownictwo.key
keys_info = KeysInfo(
    key_file="/dane/ebudownictwo.key",
    cert_file="/dane/ebudownictwo.cer",
    verify_cert_file="/dane/pz.cer",
    password_file="/dane/password.txt",
)

# create signature context
sig = BinarySignature(
    keys_info=keys_info,
    signature_method=xmlsec.Transform.RSA_SHA256,
    digest_method=xmlsec.Transform.SHA256,
)

# instantiate SOAP client
client = Client('https://pz.gov.pl/pz-services/tpSigning?wsdl', wsse=sig)

# doc to be signed
with open('/dane/dokument.xml', 'rb') as f:
    doc_data = f.read()

result = client.service.addDocumentToSigning(
    doc=doc_data,
    successURL='https://gunb.pl',
    failureURL='https://gunb.pl/fail',
    additionalInfo='gunb',
)
print(result)

