# Getting started

## MacOS

### Setup Postgres

#### Install

Installation instructions can be found here: https://goonan.io/setting-up-postgresql-on-os-x-2/. They include:

- `brew install postgresql` - Install Postgres.

#### Create database

- `psql` - confirm that you can enter the postgres shell, you may need to specify the default database name, i.e. `psql postgres`
- If your default user is not named `postgres`, create that superuser now: `CREATE ROLE rolename LOGIN SUPERUSER;`
- `create database verifact;` - create the database
- `grant all privileges on database verifact to postgres;` - give the default postgres user ownership of the new database
- The settings in verifact/settings.py by default use the above database info and should now work as expected

### Install Django

Follow the Django instructions to install Django: https://docs.djangoproject.com/en/3.1/intro/install/. Generally, you have to do the following:
- `brew install python` - Install the latest version of Python
- `brew install pipenv` - Install pipenv to isolate your python packages
- `cd <project_dir>`

### Install project dependencies

Pipenv will create a virtual environment using the correct version of python and install the needed packages into that environment. For this reason, you must always use pipenv to run python commands. Create a virtual environment and install packages using:

`pipenv install`

If you see errors relating to psycopg2, common problems include linking ssl libraries. For more information, see https://github.com/pypa/pipenv/issues/3991#issuecomment-564645309. Based on that link, you can try explicitly linking openssl using:

`export LDFLAGS="-L/usr/local/opt/openssl/lib" export CPPFLAGS="-I/usr/local/opt/openssl/include"`

Once the installation succeeds, you can move on to migrating the database.

### Configure local environment

You must have a `.env` file locally to configure certain properties when starting Django. This file is purposefly ignored from our repository, so you must create it locally. To do so, follow the steps below:

- `cp .env.test .env` - Copy .env.test to .env
- Edit the new `.env` file with your editor of choice
- Remove `DB_PASSWORD`, we didn't set a password
- Update `DB_NAME` from `postgres` to `verifact` to match the name we used above

#### Migrate the database

- `pipenv run python manage.py migrate` - You'll need to do this whenever the database has changes
- `pipenv run python manage.py createsuperuser` - Create the admin user
- Enter admin credentials, you can use "admin", "admin@example.com", "password" for username, email, password, respectively. This is just your development superuser

#### Confirm that it worked

- `pipenv run python manage.py runserver` - Start the Django development server
- Go to localhost:8000/admin and log in with your admin credentials. You should see Users and Groups
- You can also log into your postgres shell to confirm that it worked by running `psql verifact`, then once in the shell, run `\d` to show all relations. It should show a handful of django relations

#### Preload data
- `pipenv run python manage.py loaddata users questions answers votes citations` - This command loads the specified fixtures from `verifact/forum/fixtures/` into the database. To load specific fixtures, specify those fixtures at the end of the command.

# Formatting style

In order to maintain consistent formatting within this project, please use https://github.com/psf/black.

# GraphQL

GraphQL provides a single endpoint and allows us to query our entire API through that endpoint. This allows us to focus on the releationships of our data instead of designing a flexible REST API. Because it uses a graph instead of hierarchical data, we also only fetch the data we need, thereby avoiding excessive trips to the database.

To learn more about GraphQL, visit https://graphql.org/

## Relay

Relay requires a pre-defined schema in order to compile. To export a schema, run the following command:

`pipenv run python ./manage.py graphql_schema --schema verifact.schema.schema --out schema.graphql`

## GraphiQL

Graphiql is a UI interface that allows us to easily test queries. After starting up the django server (`pipenv run python manage.py runserver`), you can visit `localhost:8000/graphql` to query the API.

# Testing

We use pytest to manage tests. First, install development dependencies by running:

`pipenv install -d`

Then, start the test suite by running:

`pipenv run pytest`

We use pytest-watch to watch for changes and re-run tests on change. To start pytest-watch, run:

`pipenv run ptw`

I have run into problems with OS events not reporting correctly and the tests not being re-run after a save. If this occurs, you can use polling with a `-p` as well.

`pipenv run ptw -p`
