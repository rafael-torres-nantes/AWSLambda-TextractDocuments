# AWS Lambda - Textract

## 👨‍💻 Projeto desenvolvido por: 
[Rafael Torres Nantes](https://github.com/rafael-torres-nantes)

## Índice

* [📚 Contextualização do projeto](#-contextualização-do-projeto)
* [🛠️ Tecnologias/Ferramentas utilizadas](#%EF%B8%8F-tecnologiasferramentas-utilizadas)
* [🖥️ Funcionamento do sistema](#%EF%B8%8F-funcionamento-do-sistema)
* [🔀 Arquitetura da aplicação](#arquitetura-da-aplicação)
* [📁 Estrutura do projeto](#estrutura-do-projeto)
* [📌 Como executar o projeto](#como-executar-o-projeto)
* [🕵️ Dificuldades Encontradas](#%EF%B8%8F-dificuldades-encontradas)

## 📚 Contextualização do projeto

O projeto tem como objetivo criar uma solução automatizada para extrair texto e informações de documentos armazenados no S3 utilizando o AWS Textract. A aplicação é implementada como uma função Lambda que processa eventos do S3, extrai o texto dos documentos e retorna os dados extraídos.

## 🛠️ Tecnologias/Ferramentas utilizadas

[<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">](https://www.python.org/)
[<img src="https://img.shields.io/badge/Visual_Studio_Code-007ACC?logo=visual-studio-code&logoColor=white">](https://code.visualstudio.com/)
[<img src="https://img.shields.io/badge/Boto3-0073BB?logo=amazonaws&logoColor=white">](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[<img src="https://img.shields.io/badge/AWS-Lambda-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/lambda/)
[<img src="https://img.shields.io/badge/AWS-Textract-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/textract/)
[<img src="https://img.shields.io/badge/Dotenv-ECD53F?logo=dotenv&logoColor=white">](https://pypi.org/project/python-dotenv/)

## 🖥️ Funcionamento do sistema

### Backend

O backend da aplicação foi desenvolvido utilizando **Python** e **Boto3** para interagir com os serviços da AWS. A função Lambda é responsável por processar eventos do S3, extrair texto dos documentos usando o AWS Textract e retornar os dados extraídos.

* **Importação de Credenciais**: O arquivo `utils/import_credentials.py` contém a função para carregar as credenciais AWS a partir de um arquivo `.env`.
* **Verificação de Credenciais**: O arquivo `utils/check_aws.py` contém a classe `AWS_SERVICES` que verifica a validade das credenciais AWS.
* **Processamento de Documentos**: O arquivo `extract_info/service_textract.py` contém a classe `TextractProcessor` que utiliza o AWS Textract para extrair texto e informações de documentos armazenados no S3.
* **Função Lambda**: O arquivo `lambda_handler.py` contém a função Lambda que processa os eventos do S3 e utiliza o `TextractProcessor` para extrair texto dos documentos.

## 🔀 Arquitetura da aplicação

O sistema é baseado em uma arquitetura serverless utilizando AWS Lambda para processar eventos do S3 e AWS Textract para extrair texto dos documentos. As credenciais AWS são carregadas a partir de um arquivo `.env` e verificadas antes de serem utilizadas.

## 📁 Estrutura do projeto

A estrutura do projeto é organizada da seguinte maneira:

```
.
├── utils/
│   ├── import_credentials.py
│   ├── check_aws.py
├── extract_info/
│   ├── service_textract.py
├── lambda_handler.py
├── .env
├── .env.example
├── .gitignore
└── readme.md
```

## 📌 Como executar o projeto

Para executar o projeto localmente, siga as instruções abaixo:

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/aws-lambda-textract.git
    ```

2. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure as credenciais AWS:**
    Renomeie o arquivo `.env.example` para `.env` e insira suas credenciais AWS.

4. **Execute a função Lambda localmente:**
    Utilize uma ferramenta como o AWS SAM CLI para testar a função Lambda localmente.

## 🕵️ Dificuldades Encontradas

Durante o desenvolvimento do projeto, algumas dificuldades foram enfrentadas, como:

- **Configuração de Credenciais**: Garantir que as credenciais AWS estejam corretamente configuradas e seguras.
- **Tratamento de Erros**: Implementar tratamento de erros adequado para lidar com falhas na extração de texto e na comunicação com os serviços da AWS.
- **Otimização de Performance**: Garantir que a função Lambda processe os documentos de forma eficiente e dentro dos limites de tempo de execução.
