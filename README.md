# Startup application
- Run `docker compose up --build`

# Run Pytests
- Set pythonpath to root directory of application `export PYTHONPATH=$PWD`
- Run `python -m venv .venv`
- Run `source .venv/bin/activate`
- Run `pip install -r requirements.txt`
- Run `pytest`