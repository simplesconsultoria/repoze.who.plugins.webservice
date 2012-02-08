# -*- coding:utf-8 -*-
import unittest


class TestPlugin(unittest.TestCase):

    def setUp(self):
        self.env = self._makeEnviron()

    def _makeEnviron(self, kw=None):
        """Create a fake WSGI environment
        This is based on the same method of the test suite of repoze.who.
        """
        environ = {}
        environ['wsgi.version'] = (1, 0)
        if kw is not None:
            environ.update(kw)
        return environ

    def _getTargetClass(self):
        from repoze.who.plugins.webservice import WebServicesPlugin
        return WebServicesPlugin

    def _makeOne(self):
        klass = self._getTargetClass()

        def connect(self, req):
            _users = ['foo', 'foo_bar']
            import json
            data = json.loads(req.data)
            if data['login'] in _users and (data['login'] == data['password']):
                return '{"status": true}'
            return '{"status": false}'

        setattr(klass, '_connect', connect)
        inst = klass('http://localhost:8080/validate_user',
                                      timeout=2,
                                      login_field='login',
                                      password_field='password',
                                      response_field='status'
                                     )
        return inst

    def test_implements(self):
        from zope.interface.verify import verifyClass
        from repoze.who.interfaces import IAuthenticator
        klass = self._getTargetClass()
        verifyClass(IAuthenticator, klass)

    def test_authenticate_no_password(self):
        plugin = self._makeOne()
        self.assertEqual(plugin.authenticate({}, {'login': 'abc'}), None)

    def test_authenticate_no_login(self):
        plugin = self._makeOne()
        self.assertEqual(plugin.authenticate({}, {'password': ''}), None)

    def test_authenticate_valid_credentials(self):
        plugin = self._makeOne()
        self.assertEqual(plugin.authenticate({}, {'login': 'foo',
                                                  'password': 'foo'}), 'foo')

    def test_authenticate_invalid_username(self):
        plugin = self._makeOne()
        self.assertEqual(plugin.authenticate({}, {'login': 'doh',
                                                  'password': 'doh'}), None)

    def test_authenticate_invalid_password(self):
        plugin = self._makeOne()
        self.assertEqual(plugin.authenticate({}, {'login': 'foo',
                                                  'password': 'bar'}), None)

    def test_plugin_prepare_request(self):
        plugin = self._makeOne()
        request = plugin._prepare_request(login='foo', password='bar')

        self.assertEqual(request.data, '{"login": "foo", "password": "bar"}')

    def test_plugin_bad_response_from_backend(self):
        plugin = self._makeOne()

        def connect(req):
            # Let's return an invalid JSON
            return '{"status": false'
        plugin._connect = connect

        self.assertEqual(plugin.authenticate({}, {'login': 'foo',
                                                  'password': 'foo'}), None)
