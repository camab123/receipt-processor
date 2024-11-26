FROM python:3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --upgrade

COPY . /app

EXPOSE 80

CMD ["fastapi", "run", "api/main.py", "--port", "80"]