
# Setup

## Tooling

* Python 3.10.7 or newer (not that Python 3.10.0 will not work)

* NodeJS 16 or newer

* A POSIX-compliant system

## Main Setup

1. Git clone the project and cd into its main directory

2. Create a virtual environment by running `python -m venv .venv`

3. Activate the virtual environment using `source ./.venv/bin/activate`

4. Install Python dependencies using `pip install -r requirements.txt`

5. Install NodeJS dependencies using `npm i`

## Running Ensemble

`python scripts/run_all.py`

You can specify the URL that the backend is based on, as follows:

`python scripts/run_all.py --backend=api.some.website.example.com`

This allows the backend and frontend to run deployed to the open internet.
