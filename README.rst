============
Run Buildout
============
Clone a copy of this repo. Then::

  > cd collective_stats_logviewer 
  > /path/to/your/python bootstrap.py
  > ./bin/buildout

This may take some time as it will get all the requirements you need to un this project!

=======================
Initialize the database
=======================
Step zero: make sure your repo is up to date

Step one: (cd into collective_stats_logviewer) Type in your terminal::

  ./bin/flask-ctl debug initdb

=====================
Initialize the server
=====================
Type in your terminal::

  ./bin/flask-ctl debug fg


================
Import Test Data
================
To import test data in the current setup, run from the base of the buildout::

  ./bin/python-console scripts/file_load.py instance1.log


=======
Problem
=======
Parse through a log file from a plone instance that has collective.stats installed to pull out meaningful stats and publish to the web. Help them find long running requests, requests that are taking a lot of memory, and general performance related stats.

From the command line, send that log to a web service which will parse through it and then return a pretty url where a user can go analyze their stats. Some details:

* The framework will be Flask. You will benefit from going through the `other  <https://github.com/noisebridge/web2py-noiselist>`_ `web framework <https://github.com/noisebridge/flask-noiselist>`_ `tutorials <https://github.com/noisebridge/django_noiselist>`_ if you are not familiar with concepts of templates, databases, etc.
* It's not realistic to send whole log files through the web so start thinking about chunking techniques. This makes sense since in reality you would want this data being updated real time.
* We have minimally covered relational databases but you might want to `ramp up on the concepts <http://developer.apple.com/library/safari/#documentation/iPhone/Conceptual/SafariJSDatabaseGuide/RelationalDatabases/RelationalDatabases.html>`_ ahead of time. We will be using sqlalchemy with a lot of `ETL <http://en.wikipedia.org/wiki/Extract,_transform,_load>`_. If you guys are passionate we can be cool and try a nosql database but I don't think its best for long term job stuff.
* I expect most of you to be nominally familiar with html and we will be digging into jquery and plotting libraries. We will be rotating and pairing with who has good skills where but going through a `jQuery tutorial <http://learn.jquery.com/>`_ and a `javascript tutorial <http://autotelicum.github.com/Smooth-CoffeeScript/literate/js-intro.html>`_ would be great. 
* In haste with a client I already wrote a good chunk of the actual log parsing and that will be in this repo for reference.
.
