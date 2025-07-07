FROM python:slim

WORKDIR /app

ENV TOKEN="" ADMIN_ID=""

COPY . /app/

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]

EXPOSE 8000
