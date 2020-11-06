# Back-end FastAPI - Base Project Generator


Generate a backend and frontend stack using Python, including interactive API documentation.

## How to use it

Go to the directory where you want to create your project and run:

```bash
git clone https://laodai148148@bitbucket.org/epsilo/sms-backend.git
```

### Create python Enviroment

```bash
cd epsilo-backend

py -m venv env

```
### Install requirement packages

Go to the Back-end folder and then Install packages

```bash
cd epsilo-backend
pip install -r requirements
```


### Input configuration variables


The input  configuration variables in file epsilo-backend

* `MYSQL_SERVER`: Host Mysql server
* `MYSQL_PORT`: Connection Port
* `MYSQL_USER`: Mysql user name
* `MYSQL_PASSWORD`: Mysql user password


* `MYSQL_DB`: Schema name
* `SECRET_KEY`: Backend server secret key for create token
* `ACCESS_TOKEN_EXPIRE_MINUTES`: Expired time of Access token


### Run it

```bash
uvicorn main:app --reload

```

### install alembic migration

```bash
pip install alembic

```

###  Alembic Tnitialization


```bash
cd ..
alembic init alembic

```

### Config Alembic configuration variable

## file alembic.ini
* `sqlalchemy.url`: sqlalchemy url, ex : 'mysql+pymysql://root:Daipro184@127.0.0.1/epsilo'

## File alembic/env.py , add and replace some code on the env.py file

```python
    import sys
    import site
    site.addsitedir('path to your backend folder')
    from db.base import Base
    target_metadata = Base.metadata
```

