# XSQL
An SQL-like toy language interpreter and xml database, for learning purposes, written in python.

### Usage
Clone the repo and switch to the backend directory. Create a virtual enviroment inside:

    $ cd backend/
    $ python -m venv .venv

Start the virtual environment and install the pacakages inside requirements.txt:

    $ source .venv/bin/activate
    $ pip install -r requirements.txt

Start the backend's dev server by running:

    $ uvicorn main:app --reload

### REPL
You may also use the bundled REPL to test the program:

    $ python backend/repl.py
    # ctrl + c / ctrl + d to terminate execution

note: the REPL only parses one line at a time

### todo
- [ ] update README.md to include frontend usage

### credits
- Saul Castellanos
- Nery Jiménez
- Denis Calederón
