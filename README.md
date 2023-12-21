# XSQL
An SQL-like toy language interpreter and xml database, for learning purposes, written in python.

### Usage
Clone the repo and switch to the backend directory. Create a virtual enviroment inside:

    $ cd backend/
    $ python -m venv .venv

Start the virtual environment and install the pacakages inside requirements.txt:

    $ source .venv/bin/activate
    # .venv\Scripts\activate on Windows. 
    # Comment uvloop==0.19.0 in requirements.txt
    $ pip install -r requirements.txt

Start the backend's dev server by running:

    $ uvicorn main:app --reload
    # add '--loop asyncio' on Windows
    # uvicorn main:app --loop asyncio --reload on Windows

### REPL
You may also use the bundled REPL to test the program:

    $ python backend/repl.py
    # ctrl + c / ctrl + d to terminate execution

note: the REPL only parses one line at a time

### Frontend
switch to the frontend directory. Install dependencies
    $ cd frontend/
    $ npm install

Start the frontend's server by running
    $ npm start

### todo
- [ ] update README.md to include frontend usage

### credits
- Saul Castellanos
- Nery Jiménez
- Denis Calederón
