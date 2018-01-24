Architectural Design
====================

This document is the primary detailed design document for this task. It does _not_ contain lists of requirements or other specification information, beyond that which is required to explain the system design and implementation procedure.

Foundations
-----------

The server is a dual-CPU droplet from Digital Ocean with 2GB memory and 60GB disk space, located in Frankfurt, Germany. The operating system is Linux, variant Ubuntu 16.04 64-bit.

The server is a single, self-contained web, application and database server.

There are three distinct user groups:

1. Admin users: These are Hotjar customers who want to view and analyse the data from the surveys. They view the web-based management dashboard and can monitor the results as they come in. They may be using desktop or mobile devices.
1. Survey users: These are website end-users who answer the survey. They complete a set of questions (eight questions, presented two per web page/screen/step) and submit it for a Thank You message. They may be using desktop or mobile devices.
1. System users: This is Hotjar staff and any other stakeholders. They can access the system using SSH as well as HTTP. They also can use the platform's built-in data tools for monitoring & maintaining the system and survey responses, such as those available under MySQL and API Star. Their access, for system purposes, is expected to be via desktop/laptop devices rather than mobile devices.

#### Database

The database is MySQL 5.7.

#### Application

The application is written in Python 3, using the API Star framework. The application accesses the database using the SQLAlchemy extension.

#### Web server

The web server software is Nginx.

#### HTML/CSS/Javascript

The front-end code will primarily generate its HTML using Javascript; the management dashboard for admin users may also rely on server-side templates if/where necessary. 

The jQuery library will be used, along with underscore.js and Backbone.js (see below). Require.js will be used to optimise the loading of these Javascript libraries.

The Bootstrap suite provides a convenient, if not exceptional, shortcut to responsive design, and will be used in the rendering of the front-end.

The front-end architecture will use Backbone.js for RESTful communication with the server.

#### Process: Survey

A user clicks (?) to view the first page of the survey. This page loads the Javascript survey application from the survey, along with the list of questions. (They are separated to abide by (Hotjar best practice for optimising reloads of updated data).)

The survey application will display the relevant questions to the user. Questions which have been answered already by this user will not be displayed again. The system will rely on cookies on the client-side, and checks on the server-side, to manage these decisions.

The survey application will 'ping' the server to advise about user activity. On completion of each step, the application will send the data to the server and display the next step. The final screen will have a Thank you message.

#### Process: Admin

An admin user clicks (?) to view _their_ survey results. This loads a management dashboard with a summary information area at the top, and the detail of the survey results in a table beneath. 

The summary information area will utilise Google Visualizations where appropriate to represent the data.

The table of responses (and potentially also the summary area) will include information on surveys which are in progress / partially-completed. It should distinguish between those that are 'live' and being completed, and those which have probably been abandoned, using an idle time threshold and/or the 'pings' from the survey application code.

#### Security

The system will contain user data. The demonstration server will _not_ use SSL/HTTPS; thus the _hosting_ element will not be suitable for widespread production without appropriate certificates being procured & installed first.

The data & database will reside in the European Union.

The server runs a firewall allowing access only on ports 80 and 22. SSH access to the server is only by public key to a named user account. (Direct access to other services, such as MySQL on port 3306, can be achieved using SSH tunnels.)

Authorisation information including database passwords will be stored in the _environment_ and not in the codebase, following 12-factor app guidelines. The list of required environment variables for the system is contained in the file env.bash.example at the root level of the code repository.

Access to the web pages for the survey and management dashboards will have specific additional security measures to be determined during those delivery stages.

#### Capacity

The capacity of the system is unknown at this time but will be tested for benchmark measurements at each stage of the delivery process, and on completion of the project. The intention is that a quantified measure of estimated minimum guaranteed capacity will be available upon delivery, along with details of how that measure was reached.

At this time, tools such as Memcache and Redis, which can be used to increase system capacity further, are _not_ part of the architecture.

#### Not used

*AWS*

Although hosted on Digital Ocean, the system _should_ be compatible with _AWS Lambda_ using the Zappa wrapper, effectively allowing for serverless hosting / zero infrastructure.

*PostgreSQL*

I have experience with PostgreSQL but my expertise is undoubtedly in MySQL. Given that MySQL is an option, I have used it to minimise risk to delivery. 

It is likely that much/all of the actual SQL used to interact with the database is already compatible with PostgreSQL. A review to confirm that, or to establish the cost of translation to make the system compatible with PostgreSQL, is possible but is not in scope for this project.

*Angular*

I do not yet have working experience with Angular and would prefer to implement the front-end using other libraries. I am keen to learn Angular in a working context so I can use it in something other than the introductory exercises I have completed in the past.

*Memcache, Redis*

When implemented effectively, in-memory caches such as Memcache and Redis can significantly improve system performance. For the purposes of this demonstration, the system is _not_ augmented with these additional tools, relying instead for performance on the built-in capacity of the core platforms and the efficiency of the code they run.

#### History

24 January - First draft for feedback.
