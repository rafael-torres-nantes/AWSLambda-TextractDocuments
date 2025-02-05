# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #
# RUN LOCALY
from utils.check_aws import AWS_SERVICES

aws_services = AWS_SERVICES()

session = aws_services.login_session_AWS()
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #

import base64
import time
from typing import Dict, Any

from services.s3bucket_service import S3BucketClass

class TextractClass:
    def __init__(self):
        # Inicializa o cliente Textract
        self.textract_client = session.client('textract', region_name='us-east-1')

        # Inicializa a classe S3BucketClass
        self.s3_service = S3BucketClass()
    
    def extract_text_from_images(self, doc_base64: bytes) -> Dict[str, Any]:
        """
        Extração de texto de um documento codificado em base64 usando o AWS Textract.
        Note: Não suporta multiplas páginas em um único documento.
        
        Args:
            doc_base64 (bytes): Base64 encoded document in bytes format
            
        Returns:
            Dict[str, Any]: Textract response with extracted text
        """
        try:
            # Decodifica o base64 para bytes do documento
            document_bytes = base64.b64decode(doc_base64)
            
            # Envia para o Textract
            return self.textract_client.get_document_text_detection(
                Document={'Bytes': document_bytes}
            )
                
        except base64.binascii.Error as e:
            raise Exception(f"Erro na decodificação do base64: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao processar documento com Textract: {str(e)}")
        
    def extract_text_from_document(self, doc_base64: bytes, bucket_name: str, file_name: str) -> Dict[str, Any]:
        """
        Extrai texto de um documento PDF com várias páginas usando AWS Textract.
        
        Args:
            doc_base64 (bytes): Documento codificado em base64.
            bucket_name (str): Nome do bucket S3 para armazenar o PDF.
            file_name (str): Nome do arquivo no S3.
            
        Returns:
            Dict[str, Any]: Resposta do Textract com o texto extraído.
        """
        try:
            # Decodifica o base64 para bytes
            document_bytes = base64.b64decode(doc_base64)

            # Faz o upload do PDF para o S3
            self.s3_service.put_object(document_bytes, bucket_name, file_name)

            # Inicia o processamento do documento com várias páginas
            response = self.textract_client.start_document_text_detection(
                DocumentLocation={'S3Object': {'Bucket': bucket_name, 'Name': file_name}}
            )
            job_id = response['JobId']

            # Aguarda a conclusão do processamento
            while True:
                status_response = self.textract_client.get_document_text_detection(JobId=job_id)
                status = status_response['JobStatus']
                if status in ['SUCCEEDED', 'FAILED']:
                    break
                time.sleep(5)  # Espera 5 segundos antes de verificar novamente

            # Verifica se o processamento foi bem sucedido
            if status == 'SUCCEEDED':
                
                # Obtém todos os resultados (pode ser paginado)
                results = []
                next_token = None
                
                # Loop para obter todos os resultados
                while True:
                    if next_token:
                        response = self.textract_client.get_document_text_detection(JobId=job_id, NextToken=next_token)
                    else:
                        response = self.textract_client.get_document_text_detection(JobId=job_id)
                    
                    results.extend(response.get('Blocks', []))

                    # Verifica se há mais páginas para processar
                    next_token = response.get('NextToken')
                    if not next_token:
                        break
                
                # Deleta o arquivo do S3
                self.s3_service.delete_object(bucket_name, file_name)
                return results
            else:
                raise Exception(f"Erro ao processar documento com Textract: {status_response.get('StatusMessage', 'Status desconhecido')}")

        except base64.binascii.Error as e:
            raise Exception(f"Erro na decodificação do base64: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao processar documento com Textract: {str(e)}")
        

    def extract_all_texts(self, textract_response):
        """
        Extrai todos os textos dos blocos retornados pelo Textract.
        
        Args:
            textract_response (list): Lista de blocos retornados pelo Textract.
            
        Returns:
            list: Lista de textos extraídos.
        """
        all_texts = ""

        for block in textract_response:
            if 'Text' in block:
                all_texts += block['Text']

        return all_texts