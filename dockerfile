FROM python:3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --upgrade

COPY . /app

CMD ["fastapi", "run", "app/api/main.py", "--port", "80"]