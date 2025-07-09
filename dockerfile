FROM python:slim

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]

EXPOSE 8000
