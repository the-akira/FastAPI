from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict
from email.mime.text import MIMEText
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from sqlmodel import SQLModel
import requests
import smtplib
import re
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def validate_url(url: str) -> bool:
    # Verifica se a URL tem um formato válido
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domínio...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...ou endereço IP
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...ou IPv6
        r'(?::\d+)?'  # porta opcional
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(url_regex, url) is not None

def send_email(email: str, subject: str, message: str):
    try:
        # Configurações para o Outlook SMTP
        smtp_server = "smtp.office365.com"
        smtp_port = 587  # Porta para TLS
        smtp_user = EMAIL
        smtp_password = EMAIL_PASSWORD

        # Criando a mensagem de e-mail
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = email
        msg['Subject'] = subject  # Usando o assunto fornecido na requisição

        # Anexando a mensagem ao corpo do email
        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        # Configuração do servidor SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Inicia a criptografia TLS
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email, msg.as_string())
            print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def model_to_dict(model: SQLModel) -> Dict[str, Optional[List[str]]]:
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}

def scrape_website(url: str) -> Dict[str, Optional[List[str]]]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.string if soup.title else None
    meta_description = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_description['content'] if meta_description else None

    headings = [heading.get_text() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    links = [link['href'] for link in soup.find_all('a', href=True)]
    content = [p.get_text() for p in soup.find_all('p')]

    return {
        'title': title,
        'meta_description': meta_description,
        'headings': headings,
        'links': links,
        'content': content
    }