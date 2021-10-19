# coolpress
By **Valeri Sabev**

CoolPress is an application to show the power of web development using Django

## How to Install
We are about to find our ;P

## Commands
* django-admin startproject coolpress (to init the project)
* python manage.py startapp press (to start the app)
* python manage.py runserver (run the server / command we created)
* python manage.py makemigrations (make changes for models)
* python manage.py migrate (update the changes)
* python manage.py sqlmigrate press 0001 (to check SQL commands)
* python manage.py shell

## DB Commands
* from press.models import Category
* Category.objects
* .save()
* .object.create()

### Models
It is a bit like a table inside a database, an object