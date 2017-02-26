# Training IMage LABeler

Timlab provides an easy to use machine learning training image labeling web platform.
It differs from [LabelMe](http://labelme.csail.mit.edu/) by emphasing simplicity
and limiting labeling to whole picture instead of its parts.

## Installation

1. Check out the source code.
2. Adjust src/timlab/settings.py to suit your needs. See [Django documentation](https://docs.djangoproject.com/en/1.10/topics/settings/) for details.
3. cd to src folder
4. Install Django (if you don't have one): `pip install -r requirements.txt`
5. Create initial migrations: `./manage.py migrate projects images`
6. Apply migrations to the DB: `./manage.py migrate`
7. Create superuser of installation: `./manage.py createsuperuser`
8. Collect static files for web serving: `./manage.py collectstatic`
9. Set up Apache or any other web server - read [Django documentation](https://docs.djangoproject.com/en/1.10/howto/deployment/) for details.
For testing purposes a built-in server will be enough: `./manage.py runserver` http://localhost:8000

## Directory layout

* doc/ - documentation
* src/ - actual code
* src/project/ - training projects and their label lists
* src/image/ - images and their handling functions
* src/timlab/ - main settings
