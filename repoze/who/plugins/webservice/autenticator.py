# -*- coding:utf-8 -*-
import json
import socket
import urllib
import urllib2

from zope.interface import implements

from repoze.who.interfaces import IAuthenticator


class WebServicesPlugin(object):

    implements(IAuthenticator)

    def __init__(self, url, timeout=1,
                 login_field='login', password_field='password',
                 response_field='status'):
        self.url = url
        self.timeout = float(timeout)
        self.login_field = login_field
        self.password_field = password_field
        self.response_field = response_field

    def _prepare_request(self, login, password):
        ''' Prepare request to be send to backend as json '''
        data = {self.login_field: login,
                self.password_field: password}

        data = json.dumps(data)
        #data = urllib.urlencode(data)
        req = urllib2.Request(self.url, data)
        return req

    def _connect(self, req):
        ''' '''
        # Set timeout
        socket.setdefaulttimeout(self.timeout)
        # Connect
        response = urllib2.urlopen(req)
        return response.read()

    def _check_credentials(self, login, password):
        ''' Connects to the backend, validating login and password '''
        # Prepare the request
        req = self._prepare_request(login, password)
        # Connect to the backend
        response = self._connect(req)
        # Process response
        try:
            body = json.loads(response)
        except ValueError:
            body = {}
        return body.get(self.response_field, False)

    # IAuthenticatorPlugin
    def authenticate(self, environ, identity):
        try:
            login = identity['login']
            password = identity['password']
        except KeyError:
            return None
        if self._check_credentials(login, password):
            return login
