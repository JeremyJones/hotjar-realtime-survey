Python Developer Task
=====================
#### Jeremy Jones
#### January 2018

Installation
------------

git clone https://bitbucket.org/hotjar/dev-task-jeremy.git
cd dev-task-jeremy
cp env.bash.example env.bash
vim env.bash   <-- edit if required

cd app
pip3 install -r requirements.txt


Quickstart
----------

To run the app:

cd app
apistar run


Testing
-------

To test the app:

cd app
apistar test


Backup App
----------

The app comes bundled with a version of Quart, which is an asyncio version of Flask. To run it:

cd app
python flaskapp.py

The backup app will run on port 5000.
