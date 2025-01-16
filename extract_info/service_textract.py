import boto3
from botocore.exceptions import ClientError
from typing import Dict, List, Optional, Union

class TextractProcessor:
    def __init__(self):
        """
        Inicializa o serviço AWS Textract.
        Cria um cliente para o serviço Textract na região especificada.
        """
        # Inicializa o cliente do Textract
        self.textract_client = boto3.client('textract', region_name='us-west-2')

    def extract_text_from_document(self, bucket_name: str, document_key: str) -> Dict:
        """
        Extrai texto de um documento armazenado no S3 usando o AWS Textract.
        
        :param bucket_name: Nome do bucket S3 onde o documento está armazenado
        :param document_key: Caminho do documento no bucket S3
        :return: Dicionário contendo o texto extraído e metadados
        """
        try:
            # Configura o documento de origem no S3
            source_document = {
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': document_key
                }
            }

            # Inicia a análise do documento
            response = self.textract_client.analyze_document(
                Document=source_document,
                FeatureTypes=['TABLES', 'FORMS']
            )

            # Processa o resultado
            extracted_data = {
                'text': self._extract_text_from_blocks(response['Blocks']),
                'tables': self._extract_tables(response['Blocks']),
                'form_fields': self._extract_form_fields(response['Blocks'])
            }

            print("Extração de texto concluída com sucesso")
            return extracted_data

        except ClientError as e:
            print(f"Erro ao processar documento com Textract: {e}")
            raise

    def _extract_text_from_blocks(self, blocks: List[Dict]) -> str:
        """
        Extrai texto de blocos LINE retornados pelo Textract.
        
        :param blocks: Lista de blocos retornados pela API do Textract
        :return: Texto extraído concatenado
        """
        text_lines = []
        for block in blocks:
            if block['BlockType'] == 'LINE':
                text_lines.append(block['Text'])
        return '\n'.join(text_lines)

    def _extract_tables(self, blocks: List[Dict]) -> List[List[str]]:
        """
        Extrai tabelas do documento processado.
        
        :param blocks: Lista de blocos retornados pela API do Textract
        :return: Lista de tabelas extraídas
        """
        tables = []
        current_table = []
        
        for block in blocks:
            if block['BlockType'] == 'TABLE':
                if current_table:
                    tables.append(current_table)
                current_table = []
            
            if block['BlockType'] == 'CELL' and 'Text' in block:
                current_table.append(block['Text'])
        
        if current_table:
            tables.append(current_table)
            
        return tables

    def _extract_form_fields(self, blocks: List[Dict]) -> Dict[str, str]:
        """
        Extrai campos de formulário do documento processado.
        
        :param blocks: Lista de blocos retornados pela API do Textract
        :return: Dicionário com pares chave-valor dos campos do formulário
        """
        key_map = {}
        value_map = {}
        form_fields = {}

        # Primeiro, mapeia todos os blocos
        for block in blocks:
            if block['BlockType'] == 'KEY_VALUE_SET':
                if 'KEY' in block['EntityTypes']:
                    key_map[block['Id']] = block
                else:
                    value_map[block['Id']] = block

        # Depois, associa chaves com valores
        for block_id, key_block in key_map.items():
            value_block = None
            for relationship in key_block.get('Relationships', []):
                if relationship['Type'] == 'VALUE':
                    for value_id in relationship['Ids']:
                        value_block = value_map.get(value_id)
            
            # Se encontrou um par chave-valor, adiciona ao resultado
            if value_block:
                key = self._get_text_from_block(key_block)
                value = self._get_text_from_block(value_block)
                if key and value:
                    form_fields[key] = value

        return form_fields

    def _get_text_from_block(self, block: Dict) -> Optional[str]:
        """
        Extrai texto de um bloco específico do Textract.
        
        :param block: Bloco individual retornado pela API do Textract
        :return: Texto extraído do bloco ou None
        """
        text = ''
        if 'Relationships' in block:
            for relationship in block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        word = block.get('Text', '')
                        if word:
                            text += word + ' '
        return text.strip() if text else None