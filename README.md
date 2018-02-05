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


Demonstration
=============

Contents
--------

1. Homepage
1. Two browsers demonstration
1. Admin API
1. Implementation overview
1. Code notes
1. Performance, growth and scale 


Homepage
--------

Survey / Admin links plus a few others.

Two browsers, survey & dashboard
--------------------------------

1. One browser window to /survey
1. One browser window to /dashboard
1. Complete survey & watch dashboard

#### Survey

1. Survey sends answers in the background and handles different screens.
1. Dashboard updates on-the-fly, including deletes. Mailto.
1. Dashboard summary updates as people go.
1. Survey re-try; Reset & re-try.

#### Dashboard

1. Fields marked unique 
1. Limited, most recent results displayed
1. Columns are sortable & selectable
1. Paging is enabled
1. Live updates can be paused, esp when interacting with detail table
1. Summary pie graph is interactive
1. Summary average age is up to 1 decimal place
1. Summary surveys count is ALL. The number changes to 'k' at 10,000 (with the actual number available in a tooltip)


Admin API
---------

Built-in administrative interface at /docs which can be disabled in
production.

1. Automatic documentation from the code.
1. Ad-hoc queries and checks can be carried out in the browser.
1. The 'coreapi' utility can be used at the command-line.


Implementation Overview
-----------------------

Two HTML pages -- survey and dashboard -- each with a self-contained
Javascript app that uses Ajax to communicate with the backend
server. The backend server is an API-first server.

Survey information is captured and sent e.g. on keyup, change, blur,
in order to show real-time updates on the dashboard. The configuation
of these live updates can be revised over time.

The dashboard continually updates looking for new information and
partially-completed answers. When any of the data changes the
dashboard page updates. These live updates can be switched off by the
user, and their default configuration can be revised over time.

The server application runs in Python 3.6 with a MySQL 5.7 database
backend (through SQLAlchemy) and a caching interface (currently
memcache).

Code README contains the procedure for installing & running (exc data
platform i.e. MySQL & memcache).

Code notes
----------

The full solution is in app/ which has the following contents:

1. app.py: required name for overall application wrapper
1. lib: static image, CSS and Javascript files
1. other: line counts and other files
1. project: *Python solution*
1. requirements.txt: pip installation file
1. templates: HTML template files for survey, dashboard & homepage
1. tests: Built-in framework test script & load test scripts
1. www: Server root for Nginx proxy server

#### project/ directory

1. models/  
Database models: Question, Response, Answer  
Application models: Summariser
1. routes/  
URL routing by path & method  
Built-in backend configuration
1. settings/  
Overall application settings, including survey_id  
Database configuration through the environment  
1. utils/  
Application cache interface  
Answer & field validators
1. views/  
api/ - handlers for the API calls via Ajax  
auth/ - handlers related to authorisation & setup  
html/ - handlers for the HTML pages

#### Relevant Design Patterns

The Summariser object, in models/dashboard/, provides the summary data
used in the dashboard. Each of those five data values (including 'last
updated') is implemented using an encapsulated behaviour
(*Strategy*). Each value is currently running from a 'default'
behaviour, which can be changed over time, including optimisations,
without requiring changes to the original calling code.

A naive/informal Strategy implementation is also in place on the field
validation routines in utils/validators/.

The behavioural class which generates the 'Top Colours' value is
*inherited* from a generic 'Top Answers' class which can determine the
most popular values in any field.

#### Javascript

Unlike the Python code, the two Javascript applications are monolithic
and self-contained.


Performance, growth and scale
-----------------------------

The rest of this document lists potential solutions for scalabil deals with various 

Existing Architecture
---------------------

The current implementation contains a number of architectural & design
decisions made with scale in mind:

1. Client-logic on client (i.e. Javascript-heavy).
1. Matching the Javascript<->Python data interface (i.e. JSON) as closely as possible; avoid translation.
1. Non-HTML static content is served via whitenoise for smooth CDN upgrade path.
1. Database usage favours key lookups, lending to datastores & similar.
1. Abstracted key/value cache behaviour (currently memcache).
1. APIStar server - high-performance with asyncio upgrade option

Scaling: General
----------------

#### Aggregation of marginal gains

> "1 percent margin for improvement in everything you do."
-Dave Brailsford

#### Network traffic

1. Libraries combined, minified, optimised.
1. CDN directives on HTML pages.
1. Paths shortened.

#### General

1. Requests for HTML pages to static files. (No current usage of Jinja template variables.)
1. /questions into static file.
1. Memcache lookups.

#### Dashboard

1. Javascript poll time/control can be altered.
1. Memcache cache time can be increased.
1. Implementation of permission tokens (e.g. load-based).
1. Summary area backend (/dashdata optimisations)

#### Survey

1. Automatic answer-sending can be altered to e.g. onblur only, instead of also onchange.
1. Implementation of captchas to limit front-end abuse attempts.
1. Implementation of permission tokens to limit back-end abuse attempts.


Scaling: Infrastructure & Framework
-----------------------------------

1. Separate (cloud) servers scaled per component, esp. database.
1. CDN integration (esp for whitenoise-served static content).
1. Load balancers, multiple web & database tiers.
1. Nginx revision/replace. Static content.
1. Async upgrade, sending & receiving data on-the-fly.


Scaling: MySQL Database
-----------------------

1. Pre-calculate heavier queries, esp. average age, gender ratio.
1. Hardware.
1. Optimised server conf.
1. Reduced integer column sizes.
1. Optimised indexes e.g. substr, order.
1. INSERT DELAYED & similar.
1. Views (native or bespoke).
1. Master/Slave (master for surveys; slaves for dashboards).
1. Clustering.


#### Disk usage

The disk space requirements for the database are up to 5mb per 1,000
completed surveys.
