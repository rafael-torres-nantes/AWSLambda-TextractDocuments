# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #
# RUN LOCALY
from utils.check_aws import AWS_SERVICES

aws_services = AWS_SERVICES()

session = aws_services.login_session_AWS()

if not aws_services.check_aws_credentials():
    raise Exception("[DEBUG] Credenciais AWS não configuradas")
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #

import os
import boto3
from typing import Optional
from botocore.exceptions import ClientError

class S3BucketClass: 
    def __init__(self):
        """
        Construtor da classe S3BucketClass que inicializa o cliente S3 da sessão.
        """
        self.s3_client = session.client('s3')
        self.download_path = './tmp/' 
        os.makedirs(self.download_path, exist_ok=True)
    
    def upload_file(self, file_path: str, bucket: str, key: str) -> bool:
        """
        Função para fazer upload de um arquivo para o bucket S3

        Args:
            file_path (str): Caminho do arquivo a ser enviado
            bucket (str): Nome do bucket S3
            key (str): Nome do arquivo no bucket
        """
        try:
            # Upload do arquivo para o bucket S3
            self.s3_client.upload_file(file_path, bucket, key)
            return True
        
        except ClientError as e:
            print(f"[DEBUG] Erro ao fazer upload do arquivo para o S3: {e}")
            raise
    
    def put_object(self, file_bytes: bytes, bucket_name: str, file_name: str) -> str:
        """
        Faz o upload de um arquivo (em bytes) para um bucket S3.
        
        Args:
            file_bytes (bytes): Bytes do arquivo a ser enviado.
            bucket_name (str): Nome do bucket S3.
            file_name (str): Nome do arquivo no S3.
            
        Returns:
            str: URL do arquivo no S3.
        """
        try:
            self.s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_bytes)
            return f"s3://{bucket_name}/{file_name}"
        
        except Exception as e:
            raise Exception(f"Erro ao fazer upload do arquivo para o S3: {str(e)}")
        
    def download_file(self, bucket: str, key: str) -> bool:
        """
        Download de um arquivo do bucket S3 para o caminho especificado

        Args:
            bucket (str): Nome do bucket S3
            key (str): Nome do arquivo no bucket
        """
        # Caminho do arquivo para download
        file_path = os.path.join(self.download_path, key)

        try:
            # Download do arquivo do bucket S3
            self.s3_client.download_file(bucket, key, file_path)
            return file_path
        
        except ClientError as e:
            print(f"[DEBUG] Erro ao fazer download do arquivo do S3: {e}")
            raise e
    
    def delete_object(self, bucket: str, key: str) -> bool:
        """
        Deleta um objeto do bucket S3 especificado por chave

        Args:
            bucket (str): Nome do bucket S3
            key (str): Nome do arquivo no bucket
        """
        try:
            # Deleta o objeto do bucket S3 especificado
            self.s3_client.delete_object(Bucket=bucket, Key=key)
            return True
        
        except ClientError as e:
            print(f"[DEBUG] Erro ao deletar objeto do S3: {e}")
            raise
    
    def get_object(self, bucket: str, key: str) -> Optional[dict]:
        """
        Obter um objeto do bucket S3 especificado por chave

        Args:
            bucket (str): Nome do bucket S3
            key (str): Nome do arquivo
        """
        try:
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            return response
        
        except ClientError as e:
            print(f"[DEBUG] Erro ao obter objeto do S3: {e}")
            raise
    
    def generate_presigned_url(self, bucket: str, key: str) -> str:
        """
        Gerar uma URL pré-assinada para um objeto no bucket S3

        Args:
            bucket (str): Nome do bucket S3
            key (str): Nome do arquivo
        """
        try:
            # Gerar URL pré-assinada para o objeto no bucket S3
            presigned_url = self.s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key})
            return presigned_url
       
        except ClientError as e:
            print(f"[DEBUG] Error generating presigned URL: {e}")