# coolpress
By **Valeri Sabev**

CoolPress is an application to show the power of web development using Django

## How to Install
We are about to find our ;P
Make coolpress folder "source root" after django-admin command

## Heroku ssh (after installing the cli)
* heroku run bash -a valchy-coolpress

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
* python manage.py collectstatic
* python manage.py dumpdata --all --indent 4 --output sample_posts.json
* python manage.py loaddata sample_posts.json

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

### Models
It is a bit like a table inside a database, an object.
In the coolpress example always create the Django users before the CoolUsers.

### Views
This is where all the routing takes place.
URLs and requests get sent and received.

## Testing
Types of testing: Functional or Non-functional

Unit Testing < Integration Testing < System Testing < Acceptance Testing

### Unit Testing
* Fast tests
* Focused on a single functionality
* Coded on the core of the application
* Small functions to test features

### Integration Testing
* Mid pace tests
* Test interactions with other applications
* e.g databases, APIs, transactions, information checks
* if mocking the integration tests they become unit


### System Testing
* Slow and test the entire system
* Ususally end-to-end (e2e) modeling a user story
* e.g user login / logout, create / edit / delete / update of a post


### Acceptance Testing
* Super slow tests
* Testing entire functionalities
* Multiple user stories (many system tests)
* Acceptance usually linked with a pre-released version of product


## Test Methodologies:
**TDD** - Test Driven Development (very effective way of developing software) => first you write tests then code
**BDD** - Behaviour Driven Development (focused on why we are doing things)

### TDD - Test Driven Development 
* Is an effective way to develop software
* First you write the tests and then you fix the tests
* It is keeping the engaging of the development up
* The tests are already written when handing the new features
* Force you to think on the whole system even before developing the featues and spot desing pitfalls fast

### BDD - Behaviour Driven Development
* Require a full spec and coordination with product
* Methodology of higher level than TDD
* Focused on Why we are doing things
* Helps a lot the coordination with product department
* Uses some language that join development and Product departments
* Even Product can create the tests by them own because the statements are linked to code


### Python Test Frameworks
* UnitTests & Nose2 - used by default, very powerful, quite verbose
* Tox - for testing different python versions, used for compatibility tests


## Applied Python Course
* Day 1 - overview django and micro frrameworks, coolpress
* Day 2 - UML, models, databases, permissions, data modeling, relational fields, queries
* Day 3 - admin side, extended queries, shell, superusers
* Day 4 - views, templates / tags, styling / bootstrap, urls / parameters, middlewares, context
* Day 5 - static files, django forms, styling forms, user login, context processor, decorators
* Day 6 - class based views, CBVs detail / list / updates, template naming
* Day 7 - testing, types of tests, python / django testing frameworks
* Day 8 - deployment, github actions, automate deployment, heroku
* Day 9 - mid term exam :)