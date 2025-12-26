# Imagen base oficial de Python
FROM python:3.13.7

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /

# Copiar archivos del proyecto al contenedor
COPY . .

ENV TZ=America/Santiago
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && apt-get install -y chromium-driver chromium

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto al iniciar el contenedor
CMD ["python", "main.py"]
