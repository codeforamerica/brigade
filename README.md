# The Code for America Brigade Website

Code for America Brigades are local volunteer groups that bring together community members to help make government work better. Brigades use technology to build new tools to help with local civic issues. Code for America supports Brigade chapters with resources, tools, and access to the wider civic technology movement.

This repo is for the Brigade website [https://www.codeforamerica.org/brigade](https://www.codeforamerica.org/brigade)

## Goals
This website is meant to:
* Explain what the Brigade program is
* Help people find their local Brigade
* Show off the fine works of the Brigades
* Provide tools that help Brigade work
* Make it easy to start a new Brigade

## History

The Brigade program started in 2012 as an experiment, largely copying the success of [Chi Hack Night](https://chihacknight.org/) (known at the time as [Open Gov Hack Night](https://web.archive.org/web/20150504114341/http://www.opengovhacknight.org/)).

This website is on its third version. V1 Was a Rails site with many contributors. It served the Brigade well as it was growing. As Code for America became better at supporting the volunteer groups, we needed something different.

The [CfAPI](http://github.com/codeforamerica/cfapi) was built as reaction to how Brigades were operating themselves. We now meet them where they are, instead of trying to get them to log into our site.

V2 was powered by the CfAPI and worked great, yet was built quickly with PHP and Javascript. It was kind of a cobweb of dependent parts.

V3, the current site, is meant to simplify the code and make it easier for Brigade members to get involved in building the Brigade site.

## Project Search
The [Project Search](http://www.codeforamerica.org/brigade/projects) page is a new service we built to search across thousands of civic technology projects. Go try it out, we think its pretty useful.

Read more at [README-Project-Search.md](README-Project-Search.md)

## Installation

The Code for America Brigade site is built on [Flask](http://flask.pocoo.org/) and Python with a little bit of Javascript. The `brigade/views.py` file describes the routes. The `brigade/templates` files have the HTML templates.

Set up a [Python virtual environment](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md).

Install the [required libraries](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md#install-packages).

### Install Node and frontend dependencies with npm

    brew install node
    npm install

During development, run webpack.

    ./node_modules/.bin/webpack --watch

Then run the server in debug mode:

    python manage.py runserver

The server will be available at `http://localhost:4000/brigade/`.

or run it using [Honcho and the `Procfile`](https://github.com/codeforamerica/howto/blob/master/Procfile.md):

    honcho start

You can also run unit tests like this:

    python manage.py runtests

Contacts
--------

* Tom Dooner ([tdooner](https://github.com/tdooner))
* Andrew Hyder ([ondrae](https://github.com/ondrae))
* Tomas Apodaca ([tmaybe](https://github.com/tmaybe))

Copyright
---------

Copyright (c) 2015 Code for America.
