# Cashbox project

This is cashbox project

## Installation

```bash
cp deploy/env.md deploy/.env

python -m venv venv

source venv/bin/activate

pip install poetry

poetry install
```

## Run tests

```bash
pytest
```

## Run server

```bash
python manage.py createsuperuser

python manage.py runserver
```

## Author
[Sirojiddin Yakubov](https://github.com/yakubov9791999)