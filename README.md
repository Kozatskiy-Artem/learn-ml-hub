# Intership BackEnd

Cloning repository:
```
git clone git@github.com:Kozatskiy-Artem/intership-back.git
```
Or
```
git clone https://github.com/Kozatskiy-Artem/intership-back.git
```

## Getting started

After cloning repository from Github you have to install __poetry__

### Install __Poetry__

```
curl -sSL https://install.python-poetry.org | python3 -
```
or
```
pip install poetry
```

#### After installing poetry you have to install all project dependencies

```
poetry install
```

#### In the project root directory, create a file named `.env` with keys as in the `.env.sample` file and fill them with your values.

Create migrations:
```
poetry run python manage.py makemigrations
```
Apply migrations:
```
poetry run python manage.py migrate
```
Run tests:
```
poetry run python manage.py test
```
### Project Launch

Start the Django development server:
```
poetry run python manage.py runserver
```

#### If you previously created a virtual environment in the project root, you can use standard commands.

```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py test
```
```
python manage.py runserver
```

#### Open your web browser and navigate to http://localhost:8000/.
