from abc import ABCMeta, abstractmethod
import copy
import urllib3
from urllib.parse import urlencode
import json
from typing import Optional


class BaseRequestHandler(metaclass=ABCMeta):
    ALLOWED_REQUEST_TYPES = ['GET', 'POST', 'PUT', 'DELETE']
    TIMEOUT = 60
    HEADERS = {}
    PARAMS = {}
    BODY = {}
    METHOD = 'GET'
    FIRE_ON_INIT = True

    def __init__(self):
        self.response = None
        if self.FIRE_ON_INIT:
            self.response = self.fire_request()

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    def get_headers(self) -> dict:
        headers = copy.deepcopy(self.HEADERS)
        headers['User-Agent'] = (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/90.0.4430.85 Safari/537.36')
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

    def fire_request(self) -> any:
        self.validate_method_type()
        fields, encoded_params = self.get_params()
        http = urllib3.PoolManager()
        url = self.url
        if encoded_params:
            url += '?{}'.format(encoded_params)
        response = http.request(
            self.METHOD, url, body=self.get_body(),
            headers=self.get_headers(), fields=fields, timeout=self.TIMEOUT)
        if response.status > 400:
            raise Exception
        if self.FIRE_ON_INIT:
            self.response = response
        return self.response_handler(response)

    def validate_method_type(self) -> None:
        if self.METHOD not in self.ALLOWED_REQUEST_TYPES:
            raise ValueError

    @abstractmethod
    def response_handler(self, response) -> any:
        pass
