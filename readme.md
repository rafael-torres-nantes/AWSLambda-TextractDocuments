# Processamento de Documentos com AWS Textract com Base64

## 👨‍💻 Projeto desenvolvido por:
[Rafael Torres Nantes](https://github.com/rafael-torres-nantes)

## Índice

* 📚 Contextualização do projeto
* 🛠️ Tecnologias/Ferramentas utilizadas
* 🖥️ Funcionamento do sistema
* 🔀 Arquitetura da aplicação
* 📁 Estrutura do projeto
* 📌 Como executar o projeto
* 🕵️ Dificuldades Encontradas

## 📚 Contextualização do projeto

O projeto tem como objetivo criar uma solução automatizada para processar documentos utilizando **AWS Textract**. O sistema foi desenhado para extrair texto de documentos em formato PDF, convertê-los para base64 e processá-los com o serviço Textract da AWS para obter o texto extraído.

## 🛠️ Tecnologias/Ferramentas utilizadas

[<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">](https://www.python.org/)
[<img src="https://img.shields.io/badge/Visual_Studio_Code-007ACC?logo=visual-studio-code&logoColor=white">](https://code.visualstudio.com/)
[<img src="https://img.shields.io/badge/AWS-Textract-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/textract/)
[<img src="https://img.shields.io/badge/Boto3-0073BB?logo=amazonaws&logoColor=white">](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[<img src="https://img.shields.io/badge/Dotenv-004400?logo=python&logoColor=white">](https://pypi.org/project/python-dotenv/)

## 🖥️ Funcionamento do sistema

O sistema foi desenvolvido utilizando **Python** e faz uso do serviço **AWS Textract** para extrair texto de documentos PDF.

* **Lambda Handler**: O arquivo lambda_handler.py  contém a função lambda que processa os documentos.
* **Serviços AWS**: A integração com AWS Textract está localizada em textract_service.py.
* **Utilitários**: A pasta utils contém funções para importação de credenciais AWS e outras funções auxiliares.

## 🔀 Arquitetura da aplicação

O sistema é baseado em uma arquitetura de microserviços, onde o backend se comunica com os serviços da AWS para análise e processamento dos documentos. O AWS Textract desempenha um papel central na extração de texto dos documentos.

## 📁 Estrutura do projeto

A estrutura do projeto é organizada da seguinte maneira:

```
.
├── .env
├── .env.example
├── .gitignore
├── lambda_handler.py
├── readme.md
├── services/
│   ├── __pycache__/
│   └── textract_service.py
├── tmp/
└── utils/
    ├── __pycache__/
    ├── check_aws.py
    └── import_credentials.py
```

## 📌 Como executar o projeto

Para executar o projeto localmente, siga as instruções abaixo:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/rafael-torres-nantes/aws-textract-project.git
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as credenciais AWS:**
   Preencha o arquivo .env  com suas credenciais AWS conforme o exemplo em .env.example.

4. **Execute o lambda handler:**
   ```bash
   python lambda_handler.py
   ```

## 🕵️ Dificuldades Encontradas

Durante o desenvolvimento do projeto, algumas dificuldades foram enfrentadas, como:

- **Integração com serviços AWS:** O uso de credenciais e permissões para acessar o AWS Textract exigiu cuidados especiais para garantir a segurança e funcionalidade do sistema.
- **Extração de texto:** A implementação do processamento de documentos PDF e a conversão para base64 exigiu testes e ajustes para lidar com diferentes formatos e qualidades de arquivos.
