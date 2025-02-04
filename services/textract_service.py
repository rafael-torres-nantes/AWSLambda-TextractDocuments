# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #
# RUN LOCALY
from utils.check_aws import AWS_SERVICES

aws_services = AWS_SERVICES()

session = aws_services.login_session_AWS()
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #

import base64
from typing import Dict, Any

class TextractClass:
    def __init__(self):
        self.textract_client = session.client('textract')
    
    def extract_text_from_document(self, doc_base64: bytes) -> Dict[str, Any]:
        """
        Extract text from a base64 encoded document using AWS Textract.
        
        Args:
            doc_base64 (bytes): Base64 encoded document in bytes format
            
        Returns:
            Dict[str, Any]: Textract response with extracted text
        """
        try:
            # Decodifica o base64 para bytes do documento
            document_bytes = base64.b64decode(doc_base64)
            
            # Envia para o Textract
            return self.textract_client.detect_document_text(
                Document={'Bytes': document_bytes}
            )
                
        except base64.binascii.Error as e:
            raise Exception(f"Erro na decodificação do base64: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao processar documento com Textract: {str(e)}")