# Back-end FastAPI - Base Project Generator


Generate a backend and frontend stack using Python, including interactive API documentation.

## How to use it

Go to the directory where you want to create your project and run:

```bash
git clone https://laodai148148@bitbucket.org/epsilo/sms-backend.git
```

### Create python Enviroment

```bash
py -m venv env

```
### Install requirement packages


```bash
pip install -r requirements
```


### Input configuration variables


Create dot env file base on .env.example file.

* `MYSQL_SERVER`: Host Mysql server
* `MYSQL_PORT`: Connection Port
* `MYSQL_USER`: Mysql user name
* `MYSQL_PASSWORD`: Mysql user password
* `PROJECT_NAME`: Sim_card
* `PATH_TO_BACKEND_FOLDER`: Full path to backend folder
* `MYSQL_DB`: Schema name

### Run it

```bash
cd BACKEND
uvicorn main:app --reload

```

