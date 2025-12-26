from ScrappingViper import ScrappingViper
from DataContext import DataContext
from MailSender import MailSender
import os
import dotenv
from pathlib import Path

from dotenv import load_dotenv
#BASE_DIR = os.path.join(Path.home(), "Documents") + "/.env"

#load_dotenv(BASE_DIR)
load_dotenv()
user = os.getenv("VIPER_USER")
password = os.getenv("VIPER_PASSWORD")
db_url = os.getenv("DB_URL")
if db_url is None:
    print("No se ha encontrado la URL de la base de datos en el archivo .env")
    exit(1)
if user is None:
    print("No se ha encontrado el usuario de VIPER en el archivo .env")
if password is None:
    print("No se ha encontrado la contraseña de VIPER en el archivo .env")
    exit(1)
email = os.getenv("EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")
to = os.getenv("EMAIL_TO")
if email is None or email_password is None or to is None:
    print("No se han encontrado las credenciales de correo electrónico en el archivo .env")
    exit(1)

df = ScrappingViper.main(user, password)
if df is not None:
    DataContext.main(db_url,df)
    print("Guardado con éxito en la base de datos")
    MailSender.main(email, email_password, to, df)
    print("Se ha enviado el correo con éxito")