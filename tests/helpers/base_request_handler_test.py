from urllib.parse import urlencode

import pytest
import json
from urllib3.exceptions import MaxRetryError

from helpers.base_request_handler import BaseRequestHandler

BASE_URL = 'https://httpbin.org'


class TestClassBaseRequestHandler:
    METHODS = ['GET', 'POST', 'PUT', 'DELETE']

    class MockRequestHandler(BaseRequestHandler):
        def __init__(self, parent_init=True, **kwargs):
            if parent_init:
                super().__init__(**kwargs)
            else:
                self.relative_url = None

        @property
        def base_url(self) -> str:
            return BASE_URL

        def response_handler(self, response) -> dict:
            return response

    def test_valid_url(self):
        r = self.MockRequestHandler()
        assert r.response.status == 200

    def test_invalid_url_raises_max_retry_error(self, monkeypatch):
        monkeypatch.setattr(self.MockRequestHandler, 'base_url', 'invalid_url')
        with pytest.raises(MaxRetryError):
            self.MockRequestHandler()

    def test_fire_on_request_false(self):
        request_handler = self.MockRequestHandler(parent_init=False)
        assert request_handler.fire_request().status == 200

    def test_all_methods_returns_200(self, monkeypatch):

        status_arr = []
        for method in self.METHODS:
            monkeypatch.setattr(self.MockRequestHandler, 'METHOD', method)
            r = self.MockRequestHandler(relative_url='/{}'.format(method.lower()))
            status_arr.append(r.response.status)
        assert len(set(status_arr)) == 1
        assert status_arr[0] == 200

    def test_get_method_with_params(self, monkeypatch):
        params = {'a': 'b'}
        monkeypatch.setattr(self.MockRequestHandler,
                            'base_url', '{}/anything'.format(BASE_URL))
        monkeypatch.setattr(self.MockRequestHandler, 'METHOD', 'GET')
        monkeypatch.setattr(self.MockRequestHandler, 'PARAMS', params)
        r = self.MockRequestHandler(parent_init=False).fire_request()
        data = json.loads(r.data)
        assert data['args'] == params

    def test_post_method_with_params(self, monkeypatch):
        params = {'a': 'b'}
        encoded_params = urlencode(params)
        url = '{}/anything'.format(BASE_URL)
        monkeypatch.setattr(self.MockRequestHandler,
                            'base_url', url)
        monkeypatch.setattr(self.MockRequestHandler, 'METHOD', 'POST')
        monkeypatch.setattr(self.MockRequestHandler, 'PARAMS', params)
        r = self.MockRequestHandler(parent_init=False).fire_request()
        data = json.loads(r.data)
        url_params = data['url'].split('?')[1]
        assert url_params == encoded_params

    def test_post_method_with_other_attributes(self, monkeypatch):
        body = {'a': 'b'}
        headers = {'H': 'd'}
        url = '{}/anything'.format(BASE_URL)
        monkeypatch.setattr(self.MockRequestHandler,
                            'base_url', url)
        monkeypatch.setattr(self.MockRequestHandler, 'METHOD', 'POST')
        monkeypatch.setattr(self.MockRequestHandler, 'HEADERS', headers)
        monkeypatch.setattr(self.MockRequestHandler, 'BODY', body)
        r = self.MockRequestHandler(parent_init=False).fire_request()
        data = json.loads(r.data)

        assert data['data'] == json.dumps(body)

        # checking the headers
        assert 'H' in data['headers']
        assert data['headers']['H'] == 'd'

    def test_get_headers_when_headers_are_set(self, monkeypatch):
        mock_headers = {'h': 'd'}
        monkeypatch.setattr(self.MockRequestHandler, 'HEADERS', mock_headers)
        headers = self.MockRequestHandler(parent_init=False).get_headers()

        assert headers['h'] == 'd'
        assert headers['User-Agent'] == (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/90.0.4430.85 Safari/537.36')

    def test_get_params_for_get_delete_method(self, monkeypatch):
        mock_params = {'a': 'b'}
        handler = self.MockRequestHandler(parent_init=False)
        monkeypatch.setattr(handler, 'PARAMS', mock_params)
        fields, encoded_params = handler.get_params()
        assert fields == mock_params
        assert encoded_params is None

        monkeypatch.setattr(handler, 'METHOD', 'DELETE')
        fields, encoded_params = handler.get_params()
        assert fields == mock_params
        assert encoded_params is None

    def test_get_params_for_post_and_put_method(self, monkeypatch):
        mock_params = {'a': 'b'}
        handler = self.MockRequestHandler(parent_init=False)
        monkeypatch.setattr(handler, 'PARAMS', mock_params)
        monkeypatch.setattr(handler, 'METHOD', 'POST')
        fields, encoded_params = handler.get_params()
        assert fields is None
        assert encoded_params == urlencode(mock_params)

        monkeypatch.setattr(handler, 'METHOD', 'PUT')
        fields, encoded_params = handler.get_params()
        assert fields is None
        assert encoded_params == urlencode(mock_params)

    def test_validate_method_type(self, monkeypatch):
        handler = self.MockRequestHandler(parent_init=False)
        for method in self.METHODS:
            monkeypatch.setattr(handler, 'METHOD', method)
            handler.validate_method_type()

    def test_validate_method_type_raises_error(self, monkeypatch):
        monkeypatch.setattr(self.MockRequestHandler, 'METHOD', 'invalid')
        with pytest.raises(ValueError):
            self.MockRequestHandler(parent_init=False).validate_method_type()

    def test_init_function_with_params(self, monkeypatch):
        def mock_fire_request(self):
            return {}
        relative_url = '/relative_url'
        method = 'PUT'
        headers = {'a': 'b'}
        params = {'d': 'c'}
        body = {'f': 'g'}
        monkeypatch.setattr(self.MockRequestHandler, 'fire_request', mock_fire_request)
        handler = self.MockRequestHandler(
            relative_url=relative_url, method=method,
            headers=headers, params=params, body=body)

        assert handler.relative_url == relative_url
        assert handler.METHOD == method
        assert handler.HEADERS == headers
        assert handler.PARAMS == params
        assert handler.BODY == body
