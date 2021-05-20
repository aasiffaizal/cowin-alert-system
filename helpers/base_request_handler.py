from abc import ABCMeta, abstractmethod
import copy
import urllib3
from urllib.parse import urlencode
import json
from typing import Optional
from config import APP

CONFIG = APP['base_request_handler']


class BaseRequestHandler(metaclass=ABCMeta):
    ALLOWED_REQUEST_TYPES = ['GET', 'POST', 'PUT', 'DELETE']
    TIMEOUT = CONFIG['timeout']
    HEADERS = {}
    PARAMS = {}
    BODY = {}
    METHOD = CONFIG['default_method']

    @abstractmethod
    def __init__(self, relative_url=None, method=None, headers=None,
                 params=None, body=None):
        self.response = None
        self.relative_url = relative_url if relative_url else None
        self.METHOD = method if method else self.METHOD
        self.PARAMS = params if params else self.PARAMS
        self.HEADERS = headers if headers else self.HEADERS
        self.BODY = body if body else self.BODY
        self.response = self.fire_request()

    @property
    @abstractmethod
    def base_url(self) -> str:
        pass

    def get_headers(self) -> dict:
        headers = copy.deepcopy(self.HEADERS)
        headers['User-Agent'] = CONFIG['user_agent']
        return headers

    def get_params(self) -> (Optional[str], Optional[str]):
        fields, encoded_params = None, None
        if self.PARAMS:
            if self.METHOD in ['POST', 'PUT']:
                encoded_params = urlencode(self.PARAMS)
            else:
                fields = self.PARAMS
        return fields, encoded_params

    def get_body(self) -> Optional[str]:
        body = None
        if self.BODY:
            body = json.dumps(self.BODY).encode('utf-8')
        return body

    def fire_request(self) -> dict:
        self.validate_method_type()
        fields, encoded_params = self.get_params()
        http = urllib3.PoolManager()
        url = (self.base_url + self.relative_url
               if self.relative_url else self.base_url)
        if encoded_params:
            url += '?{}'.format(encoded_params)
        response = http.request(
            self.METHOD, url, body=self.get_body(),
            headers=self.get_headers(), fields=fields, timeout=self.TIMEOUT)
        if response.status > 400:
            raise Exception
        return self.response_handler(response)

    def validate_method_type(self) -> None:
        if self.METHOD not in self.ALLOWED_REQUEST_TYPES:
            raise ValueError

    @abstractmethod
    def response_handler(self, response) -> dict:
        pass
