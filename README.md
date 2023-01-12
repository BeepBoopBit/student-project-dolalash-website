# Do Lalash Development Walkthrough

## Requirements

- MongoDB v4.1.5
- pymongo
- dnspython

## Setting-up the Virtual Environment

```python
$python -m venv <name-of-project> .
```

Creates a virtual environment for the dolalash

---

## Activating The Virtual Environment

```python
# Activate
$.dolalash/Scripts/activate
# Deactivate
$deactivate
```

## Creating Database

```python
$python manage.py migrate
```

## Running the Application

```python
$python manage.py runserver
```

