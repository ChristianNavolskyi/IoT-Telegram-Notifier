FROM python:3.7

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt --upgrade

EXPOSE 80

ENTRYPOINT ["python", "server.py"]