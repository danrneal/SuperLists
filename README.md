# Superlists

A Django-based todo list app built entirely using test-driven development techniques. This app allows users to create a todo list and share that list with others.

## Set-up

Set-up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

You should see (env) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

Install the requirements:

```bash
pip install -U pip
pip install -r requirements.txt
```

You will need an email to send users messages for passwordless login. Set the email and password in your environment variables:

```bash
touch .env
echo EMAIL="YOU@EMAIL.COM" >> .env
echo EMAIL_PASSWORD="XXX" >> .env
```

Initialize and set up the database with the following command:

```bash
Usage: manage.py migrate
```

## Usage

Make sure you are in the virtual environment (you should see (env) before your command prompt). If not `source /env/bin/activate` to enter it.

Make sure .env variables are set:

```bash
set -a; source .env; set +a
```

Then run the server:

```bash
Usage: manage.py runserver
```

## Screenshots

![Superlists Homepage](https://i.imgur.com/QqsyuNf.png)

![A user's list page](https://i.imgur.com/aHdPClz.png)

![Passwordless Login](https://i.imgur.com/r269EhV.png)

## Deployment

For provisioning a new server see `deploy_tools/provisioning_notes.md`.

Set the host of your new server as an environment variable:

```bash
export HOST="YOU@HOST.COM"
```

You can deploy automatically to your new server using the following command:

```bash
fab deploy:host=$HOST
```

## Testing Suite

This repository contains a test suite consisting of functional tests and unit tests.

### Functional Tests

These test the program from the outside, from a user's point of view and are also known as Acceptance Tests or End-to-End Tests.

You will need [geckodriver](https://github.com/mozilla/geckodriver/releases) in your path. Alternatively, on Ubuntu:

```bash
sudo apt install firefox-geckodriver
```

You will also need phantomjs installed:

```bash
npm install -g phantomjs-prebuilt
```

Then you can run the functional tests with the following commands:

```bash
Usage: manage.py test functional_tests
Usage: phantomjs lists/static/tests/runner.js lists/static/tests/tests.html
```

#### _Note: If you are running the functional tests against an already deployed server such as a testing server you will need to set up a dummy email for your test user to test the passwordless login_

```bash
echo POP3_SSL="POP.EMAIL.COM" >> .env
echo TEST_EMAIL="THEM@EMAIL.COM" >> .env
echo TEST_EMAIL_PASSWORD="XXX" >> .env
set -a; source .env; set +a
```

### Unit Tests

These test the program from the inside, from developer's point of view. You can run them with the following commands:

```bash
Usage: manage.py test lists accounts
```

## Credit

[Test-Driven Development with Python](https://www.obeythetestinggoat.com/) by Harry J.W. Percival

## License

Superlists is licensed under the [MIT license](https://github.com/danrneal/superlists/blob/master/LICENSE).
