FROM python:3.11

COPY . /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD [ "python3", "-m" , "flask", "run"]
