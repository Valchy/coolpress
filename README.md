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

## DB Commands (in the shell)
* from press.models import <name_of_model>
* model = <name_of_model>.objects
* model.save()
* model.create()
* model.delete()
* model.get()
* model.update()
* model.values()
* model.exclude()

### Models
It is a bit like a table inside a database, an object.
In the coolpress example always create the Django users before the CoolUsers.