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
if user is None:
    print("No se ha encontrado el usuario de VIPER en el archivo .env")
    exit(1)
if password is None:
    print("No se ha encontrado la contraseña de VIPER en el archivo .env")
    exit(1)
email = os.getenv("EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")
to = os.getenv("EMAIL_TO")    
df = ScrappingViper.main(user, password)
if df is not None:
    if db_url is not None:
        DataContext.main(db_url,df)
        print("Guardado con éxito en la base de datos")
    else:
        print("No se ha encontrado la URL de la base de datos en el archivo .env")
    if email is not None and email_password is not  None and to is not None:
        MailSender.main(email, email_password, to, df)
    else:
        print("No se ha encontrado la configuración de correo en el archivo .env")