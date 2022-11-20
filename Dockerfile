FROM python:3.11-buster

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py main.py

CMD ["python", "main.py"]
