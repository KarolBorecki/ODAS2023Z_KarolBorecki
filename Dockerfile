FROM python:3.11.3-slim-buster

WORKDIR /flask

COPY . .

EXPOSE 3000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "app_runner.py"]