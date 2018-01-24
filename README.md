Python Developer Task
=====================
#### Jeremy Jones
#### January 2018

### Story

As a Hotjar user, I want to be able to see real-time survey responses coming in from a multi-step survey on my website.

### Requirements summary

**An admin screen** containing a summary of survey responses along with the individual surveys. The data should include partially-completed surveys and the screen should update automatically without manual reloads.

The table columns should contain the field names, with an additional column showing whether a survey is fully completed.

The summary section should contain the average age, the gender ratio, and top 3 colors, of all _completed_ surveys.

**An HTML page** containing a multi-step survey which submits its data to the admin page.

There should be four steps/screens with NEXT and PREVIOUS buttons between them.

There should be two questions per screen with varying input types for the answers. Some of the questions must be answered. Some may have multiple answers.

The questions & answer types should be

1. Name (text input). _Required_
1. Email (text input). _RequiredUnique_
1. Age (select popup). [possible values? minimum value?]
1. About me (textarea). Maximum length?
1. Address (text input) <-- what about multiple lines?
1. Gender (radio group). o Male o Female o Other or prefer not to answer
1. Favourite Book (text input). (Auto-searches amazon?!)
1. Favourite Colours (checkbox group). Which colours?


### Validation & UI

There should be a counter of the steps, so it's clear how many there are.

The email field should be validated by a server process.


### Notes ongoing

This section contains planning notes and other information.

#### Hosting

*Planned*

Digital Ocean - server created 22/01/18  (frankfurt,2cpu,3gb,60gb,ubuntu) ip 207.154.202.103

*Considered*

1. Local hosting
1. Raspberry PI

*Possible*

Server-less hosting on AWS Lambda, using the [Zappa](https://github.com/Miserlou/Zappa) wrapper (current blocker is just account privileges & key setup). 

#### System architecture

Front-end: Nginx
Backend: Gunicorn, Python 3
Database: MySQL 5.7

#### Frameworks

Front-end (end-user):   Bootstrap(?), backbone.js, underscore.js, jQuery. Require.js Multiple screens using JS.
Front-end (Hotjar user):    Similar. Also APIStar w templates, Google Visualizations for data? Data tables, Sparklines etc

Backend:    APIStar (w additional templates for admin screen)

#### Objects

Potentials: Question w answers; Response; Survey.

#### Other

Admin page should presumably use the **Observer Pattern**, similar to backbone notifying the server about survey changes.

The questions with their possible responses -- stored in json files for now. (Or should they be databased too?)

Security/SSL? This is user data. Data protection or GDPR legislation. (Private by default.)

Env configuration in the environment, not the codebase, following 12-factor app guidelines. Ignored file env.bash has a committed example in env.bash.example

Keep the code for the system separate from the list of questions, so the two can be independently cached eg by cdns, and then updates don't cause floods of new requests to the same logic code.
