# Getting started

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

#### Create database

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

#### Preload data
- `pipenv run python manage.py loaddata questions` - This command loads the data from `verifact/forum/fixtures/questions` into the database.

# Formatting style

In order to maintain consistent formatting within this project, please use https://github.com/psf/black.

# GraphQL

GraphQL provides a single endpoint and allows us to query our entire API through that endpoint. This allows us to focus on the releationships of our data instead of designing a flexible REST API. Because it uses a graph instead of hierarchical data, we also only fetch the data we need, thereby avoiding excessive trips to the database.

To learn more about GraphQL, visit https://graphql.org/

## GraphiQL

Our schema has graphiql enabled to allow us to test queries easily. After starting up the django server (`pipenv run python manage.py runserver`), you can visit `localhost:8000/graphql` to query the API.
