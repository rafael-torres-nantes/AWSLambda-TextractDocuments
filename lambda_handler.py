from extract_info.service_textract import TextractProcessor

def lambda_handler(event, context):
    try:
        # Inicializa o processador do Textract
        textract = TextractProcessor()
        
        # Extrai informações do evento
        bucket_name = event['bucket']
        document_key = event['document_key']
        
        # Processa o documento
        result = textract.extract_text_from_document(bucket_name, document_key)
        
        return {
            'statusCode': 200,
            'body': result
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }