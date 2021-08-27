# FootBallPage
GeoComply


README.md 

Setup Python

Install Django
	Set up virtual env : 
		pipenv install Django
		pipenv install six
		pipenv shell
Setup env Django
	pip install django-environ


Set up MySQL to enviroment ( Windows)
- Search google

Connect MySQL to Django

- pip install mysqlclient
- CREATE DATABASE 'name_db'
- Update information DATABASE field in 'settings.py'
- python manage.py makemigrations
- python manage.py migrate
Login = Facebook: 
- Your own Facebook account.
- use social-auth-app-django
- Python3 
- Pipenv
	+ pipenv shell 
	+ pipenv install django social-auth-app-django
If you have see MySQLdb -> set up: pip install pymysql
python -m pip install Pillow

http -> https: 
	pip install django-sslserver
	
	Add the application to your INSTALLED_APPS:

	INSTALLED_APPS = (...
	"sslserver",
	...
	)
	python manage.py runsslserver

If have error "Table 'django.social_auth_usersocialauth' doesn't exist"

After update in settings.py, please run command lines :
	python manage.py makemigration
	python manage.py migrate

The another day, You can have error :  
No module "ssqserver", run command line:
	pip install django-sslserver
No module "social-auth", run command line: 
	pip install python-social-auth[django]

Django-alert : 
	pip install django-alert

	

