# Buckley

A blogging tool built for Google App Engine with the goal of high performance and flexibility

## Features

 * Support for posts and pages
 * SEO-friendly stub URLs
 * Simple and extensible template system (based on Django templating)
 * Simple default template you can use as a base
 * Plugin system that is easy to use
 * Support for JSON and XML output 
 * REST interface to all posts and pages

## Install

Get the App Engine SDK:

  http://code.google.com/appengine/downloads.html

Check this code out into a dir. cd into that dir and edit blog.yaml to fit your settings.

Edit the template at ./templates/ or make your own copy in that dir (and update blog.yaml to use it)

To run the app, cd in and run:

  dev_appserver.py .

To deploy, use appcfg.py or the GUI that comes with Google App Engine.

Easy!

## Todo

@TODO   blog setup yaml file
@TODO   cleanup object model
@TODO	add a sidebar & cleanup style
@TODO	support for Atom & RSS feeds
@TODO	categories
@TODO	export / import
@TODO	comments / users / moderation
@TODO 	multi templates
@TODO	support multiple URLs (ie. stub changed) with list of 'old' to match and redirect
@TODO	timezone support with pytz (import pytz)
