# Development Setup

## Tooling

- VS Code with the following extensions

  - Python

  - Python Indent

  - AutoDocstring

  - MyPy

  - Code Spell Checker

  - Todo Tree

  - SQLite Viewer

- Python 3.10

- JS/TS dependencies

## Main Setup

1. Git clone the project

## Back-end

1. In VS Code's integrated terminal, create a virtual environment
   `python -m venv .venv`

2. When VS Code gives the popup, choose to activate the virtual environment

3. Restart the terminal

4. Install the dependencies `pip install -r requirements.txt`

TODO: Database setup

## Front-end

1. Navigate to the base repository folder in a terminal

2. Install the dependencies `npm i`

3. To run the application on localhost:3000 run `npm start`

4. If you see the error `ERROR in [eslint] Plugin "react" was conflicted between "package.json » eslint-config-react-app » ...base.js and "BaseConfig » ...\base.js".`, in VSCode click file > open and open the `capstone-project-h18a-ensemble` folder before running npm start in terminal. This seems to be a windows specific problem to do with pathname case sensitivity. (Previous solution was to save package.json while the app is running)

5. To test the frontend (does not require npm start) run `npm test`
