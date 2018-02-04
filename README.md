Python Developer Task
=====================
#### Jeremy Jones

Installation
------------

```
git clone https://bitbucket.org/hotjar/dev-task-jeremy.git
cd dev-task-jeremy
virtualenv --python=python3.6 venv
source venv/bin/activate
pip3 install -r app/requirements.txt
```

Quickstart
----------

To run the app:

```
cd app
apistar run
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
