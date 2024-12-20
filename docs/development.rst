=======================
Developing django-bulla
=======================

Development
-----------

1. Install distribution prerequisites

    python -m pip install setuptools
    python -m pip install build

2. Install requirements.
    (venv) pip install -r requirements_dev.txt

3. Run tests
    (venv) python manage.py test

Build the Django app
--------------------

1. Build the distribution artifacts

    python -m build


Build documentation
-------------------

1. Build the documentation using sphinx

    sphinx-build -M html docs docs-dist
