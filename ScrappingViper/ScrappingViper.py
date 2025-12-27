from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import os
from pathlib import Path
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.edge.service import Service
from selenium.webdriver.chrome.service import Service


options = webdriver.ChromeOptions()
#options = webdriver.EdgeOptions()

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--enable-chrome-browser-cloud-management')
#BASE_DIR = os.path.join(Path.home(), "Documents")
#driver_path = os.path.join(BASE_DIR, "..", "msedgedriver.exe")
#service = Service(executable_path=driver_path)
options.binary_location = "/usr/bin/chromium"
service = Service("/usr/bin/chromedriver")


#driver = webdriver.Edge(service=service, options=options) # Modificar para el que use
driver = webdriver.Chrome(service=service, options=options)


def getInfo(li, user, password):
    driver.get(li)
    wait = WebDriverWait(driver, 60)
    try:
        # Usuario
        campo_usuario = wait.until(
            EC.presence_of_element_located((By.NAME, "user"))
        )
        campo_usuario.send_keys(user)

        # Contraseña
        campo_contrasena = driver.find_element(By.NAME, "clave")
        campo_contrasena.send_keys(password)

        # Esperar que el botón exista
        boton = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )

        # Forzar scroll
        driver.execute_script("arguments[0].scrollIntoView(true);", boton)

        # Forzar click (saltándose overlays)
        driver.execute_script("arguments[0].click();", boton)

    except Exception as e:
        print("Error clicking the button:", e)
        
    wait = WebDriverWait(driver, 60)
    wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.bloque_persona.bloque_persona20"))
    )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    dataFrame = pd.DataFrame(columns=['Nombre', 'Cargo', 'N Registro', 'Estado', 'Fecha registro'])
    personsTable = soup.find_all('div', 'bloque_persona bloque_persona20')
    if personsTable:
        for person in personsTable:
            try:
                result_list = []
                person_name = person.find('div', 'persona_info persona_nombre')
                person_rank = person.find('div', 'persona_info persona_cargo')
                person_number = person.find('div', 'persona_info persona_registro')
                person_status = person.find('div', 'boton_disponible')
                person_hour = soup.find('div', id="txt_hora")
                person_day = soup.find('div', id="txt_fecha")
                person_date = person_day.text + ", " + person_hour.text
                months = {
                    "Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04",
                    "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08",
                    "Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"
                }
                partes = person_date.split(" de ")
                day = partes[0]
                month = months[partes[1]]
                year, hour = partes[2].split(", ")
                person_date_format = f"{year}-{month}-{day} {hour}"
                if person_name == "" or person_name is not None:
                    result_list.extend([person_name.text, person_rank.text, person_number.text, 
                                        person_status.text, person_date_format])
                    dataFrame.loc[len(dataFrame)] = result_list
            except AttributeError as e:
                print("Error con persona " + person_name.text)
    else:
        dataFrame = None
    return dataFrame

def main(user, password):
    link = "https://crew.viper.cl"
    new_df = getInfo(link, user, password)
    driver.quit()
    if new_df is None or new_df.empty:
        print("No se encontraron guardianes o hubo un error")
        return None
    """
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    csvName = f"Registro_Guardia_{date.strftime('%d-%m-%Y')}.csv"
    documentsDirectory = os.path.join(os.environ['USERPROFILE'], 'Documents') + '/Registro_Guardia'
    os.makedirs(documentsDirectory, exist_ok=True)
    fileRoute = os.path.join(documentsDirectory, csvName)

    new_df.to_csv(fileRoute, sep = ';', index=False)
    """
    return new_df