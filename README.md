# FLight Booking Backend Server

## How to run the application?

1. Clone the project to your folder
2. Create virtual environment for python, For example with virtualenv:
  - `python -m pip install --user virtualenv`
  - `python -m virtualenv`
3. Run file activate.bat **(for Windows)** in folder venv:
  - `./venv/Scripts/activate`
4. Download all dependencies for the projects by:
  - `pip3 install -r requirements.txt`
5. Run the applications:
  - `uvicorn index:app --reload`
6. Navigate to **/docs** route to access swagger docs

## Clients-Server Architecture

![clients-server architecture](/assets/architecture.png)



