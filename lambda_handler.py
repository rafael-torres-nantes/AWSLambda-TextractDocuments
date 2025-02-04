import os
import base64
from dotenv import load_dotenv
from services.textract_service import TextractClass

load_dotenv()

def lambda_handler(event, context):
    """
    Lambda handler para processar documentos com Textract usando base64.
    """
    textract_service = TextractClass()

    # 1. Lê o arquivo PDF e converte para base64
    file_path = './tmp/teste.pdf'
    with open(file_path, 'rb') as file:
        # Converte PDF para base64
        document_base64 = base64.b64encode(file.read())
        
        # O base64 precisa ser bytes, não string
        if isinstance(document_base64, str):
            document_base64 = document_base64.encode('utf-8')

    # Debug para verificar o base64
    print(f'[DEBUG] Base64 (primeiros 100 caracteres): {document_base64[:100]}')

    # 2. Processa com Textract
    response = textract_service.extract_text_from_document(document_base64)
    print(f'[DEBUG] Texto extraído: {response}')
    
    return response

lambda_handler(None, None)