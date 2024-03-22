# Insurance-Flask-Project
- Objective: Build an IPMS using Flask to showcase a full-stack development approach, from server-side logic with Flask to database interactions and RESTful API services, focused on insurance operations.

## Create virtual environment
- Creates a copy of your current python
    - ```bash python -m venv myen ```
- ```.\myenv\Scripts\Activate.ps1``` -> activate -> python -> local copy of python
- ```deactivate``` -> python -> global python installed
- Create a gitignore file and insert "myenv" so that it ignores any changes in the myenv folder.

## Installing Flask
- Make sure your env is activated, then install flask: [ref](https://flask.palletsprojects.com/en/3.0.x/installation/)
```sh
pip install flask
```

## How to run flask
- Make sure you are in the src folder.
```sh
cd src
```
- Running the actual flask file
```sh  
flask run 
```

- For development:
```sh  
flask run  --debug
```

## REFERENCES
- https://feliperego.github.io/blog/2019/01/11/Creating-Fake-Mock-Data-Python
- https://www.kaggle.com/code/sagarsharma4244/complete-insurance-data-analysis
- 