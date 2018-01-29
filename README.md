Python Developer Task
=====================
#### Jeremy Jones
#### January 2018

Installation
------------

```
git clone https://bitbucket.org/hotjar/dev-task-jeremy.git
cd dev-task-jeremy
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
