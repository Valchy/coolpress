# coolpress
By **Valeri Sabev**

CoolPress is an application to show the power of web development using Django

## How to Install
We are about to find our ;P
Make coolpress folder "source root" after django-admin command

## Commands
* django-admin startproject coolpress (to init the project)
* python manage.py startapp press (to start the app)
* python manage.py runserver (run the server / command we created)
* python manage.py createsuperuser
* python manage.py makemigrations (make changes for models)
* python manage.py migrate (update the changes)
* python manage.py sqlmigrate press 0001 (to check SQL commands)
* python manage.py loaddata <name_of_file_without.\>
* python manage.py shell
* python manage.py flush

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

* print(model.values('category__label').query) => prints the SQL query
* model.values()[:3] => returns the top three ones only
* model.last().delete() => deletes last entity
* model.order_by('-last_update') => orders in reverse order

* python manage.py dumpdata --all --indent 4 --output sample_posts.json
* python manage.py loaddata sample_posts.json

### Models
It is a bit like a table inside a database, an object.
In the coolpress example always create the Django users before the CoolUsers.