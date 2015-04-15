# The Code for America Brigade Website

Code for America Brigades are local volunteer groups that bring together community members to help make government work better. Brigades use technology to build new tools to help with local civic issues. Code for America supports Brigade chapters with resources, tools, and access to the wider civic technology movement.

This repo is for the Brigade website [https://www.codeforamerica.org/brigade](https://www.codeforamerica.org/brigade)

## Goals
This website is meant to:
* Get you to sign up for your local Brigade
* Explain what the Brigade program is
* Show off the fine works of the Brigades
* Provide tools that help Brigade work

## History

The Brigade program started in 2012 as an experiment, largely copying the success of [Open Gov Hack Night](http://opengovhacknight.org/). 

This website is on its third version. V1 Was a Rails site with many contributors. It served the Brigade well as it was growing. As Code for America became better at supporting the volunteer groups, we needed something different.

The [CfAPI](http://github.com/codeforamerica/cfapi) was built as reaction to how Brigades were operating themselves. We now meet them where they are, instead of trying to get them to log into our site.

V2 was powered by the CfAPI and worked great, yet was built quickly with PHP and Javascript. It was kind of a cobweb of dependent parts.

V3, the current site, is meant to simplify the code and make it easier for Brigade members to get involved in building the Brigade site.

## Installation

The Code for America Brigade site is built on [Flask](http://flask.pocoo.org/) and Python with a little bit of Javascript. The `app.py` file describes the routes. The `templates` have the html.

* Set up a [virtualenv](https://pypi.python.org/pypi/virtualenv)

```
pip install virtualenv
virtualenv .venv
source .venv/bin/activate
```

* Install the required libraries

```
pip install -r requirements.txt
```

* To run locally

```
python app.py
```

Contacts
--------

* Andrew Hyder ([ondrae](https://github.com/ondrae))

Copyright
---------

Copyright (c) 2015 Code for America.
