============
django-bulla
============

django-bulla is a Django app to add support for double-entry bookkeeping.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "bulla" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_bulla",
    ]

2. Run ``python manage.py migrate`` to create the models.

Development
-----------

1. Install distribution prerequisites

    python -m pip install setuptools
    python -m pip install build

2. Install requirements.
    (venv) pip install -r requirements.txt