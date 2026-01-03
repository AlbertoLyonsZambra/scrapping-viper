import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
from datetime import timedelta, datetime


def SendMail(email, email_password, body, subject, to):
    message = MIMEMultipart()
    message['From'] = email
    message['To'] = to
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))
    
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    
    try:
        servidor.login(email, email_password)
        
        texto = message.as_string()
        servidor.sendmail(email, message["To"].split(","), texto)
        print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error al enviar correo: {e}")
    finally:
        servidor.quit()

def main(email, email_password, to, df):
    body = ""
    subject = "Registro guardia nocturna " + (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')
    if not df.empty:
        for index,row in df.iterrows():
            body += f"{row['Nombre']},\n"
    else:
        body = "No hay guardianes o ocurrió un error"
    SendMail(email, email_password, body, subject, to)