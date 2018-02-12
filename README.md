Python Developer Task
=====================
#### Jeremy Jones
#### January 2018

Installation
------------

```
git clone https://bitbucket.org/hotjar/dev-task-jeremy.git
cd dev-task-jeremy
virtualenv --python=python3.6 venv
source ./venv/bin/activate
pip3 install -r app/requirements.txt
```

Quickstart
----------

To run the app:

```
cd app
apistar run
```

Testing
-------

To test the app:

```
cd app
apistar test
```

Command-line interface (CLI)
----------------------------

To use the command-line interface to the API, install coreapi-cli:

```
pip install coreapi-ali
```

and then load the schema:

```
coreapi get http://localhost/docs/schema/
```

and from there you can query the system application, retrieve views, and make changes:

```
coreapi action get_questions
```

Scaling
-------

The app is designed to scale in the following ways:

* The front-end tier - a proxy server on port 80, currently a single
  Nginx process - can be upgraded to a set of servers or load
  balancers.
* The app can be run from Flask and wrapped in the Quart
  framework, providing async features to the application. See
  app/flaskapp.py for starters.


Issues
------

# PEP-8 compliance
# HTTP return statuses do not match result (eg. simulated 304)
# Normalised database schema & non-self-contained stored data
  structures could lead to issues around consistency.
# 74 genders in Facebook's preferences
# Storage of data before the user has clicked Next to confirm
  their intention to submit data
# The use of transactional HTTP leads to frequent polling, whereas
  push notifications can be achieved using websockets
# Errors in the models eg. String type on an id
# Using Google viz tables, and relying on its interface for updating
  and handling large data sets (ie. paging), instead of using
  eg. Twitter-style feed updates, introduces usability and UX issues
# The two Javascript applications would benefit from refactoring and
  re-implementation to improve their efficiency and maintainability
