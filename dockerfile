FROM python:3.13

WORKDIR /server

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --upgrade

COPY ./app /server/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]