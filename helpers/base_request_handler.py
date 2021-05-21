from abc import ABCMeta, abstractmethod
import copy
import urllib3
from urllib.parse import urlencode
import json
from typing import Optional, List, Tuple
from custom_types import JsonType
from config import APP

CONFIG = APP['base_request_handler']


class BaseRequestHandler(metaclass=ABCMeta):
    ALLOWED_REQUEST_TYPES: List[str] = ['GET', 'POST', 'PUT', 'DELETE']
    TIMEOUT = CONFIG['timeout']
    HEADERS: JsonType = {}
    PARAMS: JsonType = {}
    BODY: JsonType = {}
    METHOD: str = CONFIG['default_method']

    @abstractmethod
    def __init__(
        self, relative_url: str = None,
        method: str = None,
        headers: JsonType = None,
        params: JsonType = None,
        body: JsonType = None
    ) -> None:
        self.response = {}
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

    def get_headers(self) -> JsonType:
        headers = copy.deepcopy(self.HEADERS)
        headers['User-Agent'] = CONFIG['user_agent']
        return headers

    def get_params(self) -> Tuple[Optional[JsonType], Optional[str]]:
        fields, encoded_params = None, None
        if self.PARAMS:
            if self.METHOD in ['POST', 'PUT']:
                encoded_params = urlencode(self.PARAMS)
            else:
                fields = self.PARAMS
        return fields, encoded_params

    def get_body(self) -> Optional[bytes]:
        body = None
        if self.BODY:
            body = json.dumps(self.BODY).encode('utf-8')
        return body

    def fire_request(self) -> JsonType:
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
    def response_handler(self, response) -> JsonType:
        pass
