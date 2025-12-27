FROM python:3.13

WORKDIR /

COPY . .

ENV TZ=America/Santiago
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && apt-get install -y chromium-driver chromium

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
