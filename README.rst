===============================================
repoze.who.plugins.webservice
===============================================

.. contents:: Table of Contents
   :depth: 2


Overview
--------

**repoze.who.plugins.webservice** is a repoze.who to authenticate an userid
based on information available on a backend accessible via webservice.


Usage
------

Using a who config file:
::

   [plugin:webservice]
   use = repoze.who.plugins.webservice:WebServicesPlugin
   url = http://foobar:8080/validate_user
   timeout = 2
   login_field = login
   password_field = password
   response_field = status

   [authenticators]
   plugins = webservice

