FROM python:3

WORKDIR /app

# See https://hub.docker.com/_/python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]

