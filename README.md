# Getting Started

## MacOS

### Install Django

Follow the Django instructions to install Django: https://docs.djangoproject.com/en/3.1/intro/install/. Generally, you have to do the following:
- `brew install python` - Install the latest version of Python
- `brew install pipenv` - Install pipenv to isolate your python packages
- `cd <project_dir>`
- `pipenv install` - Create a virtual environment
- `pipenv install Django` - Install the Django official release
- `pipenv run python manage.py runserver` - start the Django development server
- Visit localhost:8000, you should see a Django landing page

### Setup Postgres

#### Install

https://goonan.io/setting-up-postgresql-on-os-x-2/

- `brew install postgresql` - Install Postgres
- `pipenv install psycopg2` - Allows Django to work with Postgres

#### Create Database

- `psql` - confirm that you can enter the postgres shell
- `create database verifact;` - create the database
- `grant all privileges on database verifact to postgres;` - give the default postgres user ownership of the new database
- The settings in verifact/settings.py by default use the above database info and should now work as expected

#### Migrate the database

- `pipenv run python manage.py migrate` - You'll need to do this whenever the database has changes
- `pipenv run python manage.py createsuperuser` - Create the admin user
- Enter admin credentials, you can use "admin", "admin@example.com", "password" for username, email, password, respectively. This is just your development superuser

#### Confirm that it worked

- `pipenv run python manage.py runserver` - Start the Django development server
- Go to localhost:8000/admin and log in with your admin credentials. You should see Users and Groups
- You can also log into your postgres shell to confirm that it worked by running `psql verifact`, then once in the shell, run `\d` to show all relations. It should show a handful of django relations
